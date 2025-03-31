from networks import Actor, Critic
from envs.env import Env

import torch.torch_version
import torch
from torch.distributions import MultivariateNormal
from datetime import datetime


class PPO:
    def __init__(self, env, steps_per_trajectory, n_epochs_per_training_step, n_trajectories_per_training_step, lr_actor, lr_critic, epsilon, prefix_saved_model, std) -> None:
        current_datetime = datetime.now()
        current_datetime_str = current_datetime.strftime("%Y_%m_%d_%H_%M")
        self.env: Env = env
        self._init_hyperparameters(steps_per_trajectory=steps_per_trajectory, n_epochs_per_training_step=n_epochs_per_training_step, n_trajectories_per_training_step=n_trajectories_per_training_step, lr_actor=lr_actor, lr_critic=lr_critic, epsilon=epsilon, std=std)
        self.actor = Actor(self.env.Dimensions.observations_dims, self.env.Dimensions.actions_dims)
        self.actor_opt = torch.optim.Adam(self.actor.parameters(), lr=self.lr_actor)
        self.actor_saved_filename = f"/garage_back_end/projects/ppo/saved_models/{current_datetime_str}_{prefix_saved_model}_saved_actor"
        self.critic = Critic(self.env.Dimensions.observations_dims)
        self.critic_opt = torch.optim.SGD(self.critic.parameters(), lr=self.lr_critic)
        self.critic_saved_filename = f"/garage_back_end/projects/ppo/saved_models/{current_datetime_str}_{prefix_saved_model}_saved_critic"
        self.policy_dist = MultivariateNormal(torch.zeros(self.env.Dimensions.actions_dims), self.cov_mat)

    def _init_hyperparameters(self, steps_per_trajectory, n_epochs_per_training_step, n_trajectories_per_training_step, lr_actor, lr_critic, epsilon, std) -> None:
        self.steps_per_trajectory = steps_per_trajectory
        self.gamma = 0.95
        self.lambd = 0.5
        self.n_epochs_per_training_step = n_epochs_per_training_step
        self.n_trajectories_per_training_step = n_trajectories_per_training_step
        self.epsilon = epsilon
        self.lr_actor = lr_actor
        self.lr_critic = lr_critic
        cov_var = torch.full(size=(self.env.Dimensions.actions_dims,), fill_value=std**2)
        self.cov_mat = torch.diag(cov_var)

    def train(self, total_training_steps):
        step = 0
        while step < total_training_steps:
            print(f"-------------- training steps = {step+1}/{total_training_steps} --------------")
            obs_buffer = torch.zeros(size=(self.n_trajectories_per_training_step, self.steps_per_trajectory + 1, self.env.Dimensions.observations_dims))
            acts_buffer = torch.zeros(size=(self.n_trajectories_per_training_step, self.steps_per_trajectory, self.env.Dimensions.actions_dims))
            rews_buffer = torch.zeros(size=(self.n_trajectories_per_training_step, self.steps_per_trajectory, 1))
            log_prob_buffer = torch.zeros(size=(self.n_trajectories_per_training_step, self.steps_per_trajectory, 1))
            for trajectory in range(self.n_trajectories_per_training_step):
                # print(f"rollout {rollout+1}/{self.n_trajectories_per_training_step}")
                obs, acts, rews, log_prob = self.rollout()
                # self.env.plot_rollout(obs)
                obs_buffer[trajectory, :, :] = obs
                acts_buffer[trajectory, :, :] = acts
                rews_buffer[trajectory, :, :] = rews.unsqueeze(-1)
                log_prob_buffer[trajectory, :, :] = log_prob.unsqueeze(-1)

            print(f"avg reward per trajectory = {rews_buffer.sum()/self.n_trajectories_per_training_step} mean action = {acts_buffer.sum()/acts_buffer.nelement()}")
            advantages_buffer, rews2go_buffer = self.compute_advantages_and_rews2go(rews_buffer=rews_buffer, obs_buffer=obs_buffer)
            for epoch in range(self.n_epochs_per_training_step):
                actor_loss = self.update_actor(log_prob_before_buffer=log_prob_buffer, obs_buffer=obs_buffer, advantages_buffer=advantages_buffer, acts_buffer=acts_buffer)
                critic_loss = self.update_critic(obs_buffer=obs_buffer, rews2go_buffer=rews2go_buffer)
                print(f"epoch: {epoch}/{self.n_epochs_per_training_step} actor loss = {actor_loss} critic loss = {critic_loss}")
            if step % 10 == 0:
                self.save(f"step_{step}_total_steps_{total_training_steps}")
            step += 1

    def rollout(self):
        obs = []
        acts = []
        rews = []
        log_probs = []
        self.randomize_initial_state()
        s = self.env.get_observations()
        obs.append(s)
        # print("---------------")
        # print(f"s = {s}")
        for step in range(self.steps_per_trajectory):
            a, log_prob = self.compute_actions_sample(s)
            # print(f"a = {a} log_prob = {log_prob}")
            s = self.env.step(a)
            # print(f"s = {s}")
            r = self.env.get_reward(s, a)
            # print(f"r = {r}")
            acts.append(a)
            obs.append(s)
            rews.append(r)
            log_probs.append(log_prob)
        # print("---------------")
        return torch.stack(obs), torch.stack(acts), torch.stack(rews), torch.stack(log_probs)

    def compute_advantages_and_rews2go(self, rews_buffer: torch.Tensor, obs_buffer: torch.Tensor) -> torch.Tensor:
        advantages = torch.tensor(data=[])
        rews2go = torch.tensor(data=[])
        for step in reversed(range(self.steps_per_trajectory)):
            # print(f"step={step}")
            next_observation = obs_buffer[:, step + 1, :]
            observation = obs_buffer[:, step, :]
            delta = rews_buffer[:, step, :] + self.gamma * self.read_value_function(next_observation) - self.read_value_function(observation)  # to check again
            advantage = delta # + (self.gamma * self.lambd) * advantages[:, 0, :] if len(advantages) != 0 else delta
            advantage = advantage.unsqueeze(1)
            # normalize advantages
            mean = torch.mean(advantage)
            std = torch.std(advantage)
            advantage = (advantage - mean) / std
            advantages = torch.cat((advantage, advantages), dim=1) if advantages.nelement() != 0 else advantage
            rew2go = rews_buffer[:, step, :] + self.gamma * (rews2go[:, 0, :]) if len(rews2go) != 0 else rews_buffer[:, step, :] + self.gamma * self.read_value_function(next_observation)
            rew2go = rew2go.unsqueeze(1)
            rews2go = torch.cat((rew2go, rews2go), dim=1) if rews2go.nelement() != 0 else rew2go
        return advantages, rews2go

    def update_actor(self, log_prob_before_buffer: torch.Tensor, obs_buffer: torch.Tensor, advantages_buffer: torch.Tensor, acts_buffer: torch.Tensor) -> None:
        loss = 0
        for traj in range(self.n_trajectories_per_training_step):
            for step in range(self.steps_per_trajectory):
                action = acts_buffer[traj, step, :]
                observation = obs_buffer[traj, step, :]
                log_prob = self.compute_log_prob(action, observation)
                ratio = torch.exp(log_prob - log_prob_before_buffer[traj, step].detach())
                # print(f"ratio={ratio}")
                advantage = advantages_buffer[traj, step].squeeze().detach()
                if advantages_buffer[traj, step, 0] >=0 :
                    g = (1+self.epsilon)*advantages_buffer[traj, step, 0].detach()
                else:
                    g = (1-self.epsilon)*advantages_buffer[traj, step, 0].detach()
                loss += torch.min(ratio*advantage, g)
        self.actor_opt.zero_grad()
        (-loss).backward()
        # print(self.actor_opt.param_groups[0]['params'][0].grad)
        self.actor_opt.step()
        # print(f"loss = {loss}")
        return loss.item()

    def update_critic(self, obs_buffer: torch.Tensor, rews2go_buffer: torch.Tensor) -> None:
        predicted_V = self.read_value_function(obs=obs_buffer[:, :-1, :])
        critic_loss: torch.Tensor = torch.nn.MSELoss()(predicted_V, rews2go_buffer.detach())
        self.critic_opt.zero_grad()
        critic_loss.backward()
        self.critic_opt.step()
        return critic_loss.item()

    def read_value_function(self, obs: torch.Tensor) -> float:
        return self.critic(obs)

    def compute_actions_inference(self, obs: torch.Tensor) -> torch.Tensor:
        actions =  self.actor(obs) * self.env.get_action_constraints()
        return actions
    
    def compute_actions_sample(self, obs: torch.Tensor) -> torch.Tensor:
        mean =  self.actor(obs) * self.env.get_action_constraints()
        policy_dist = MultivariateNormal(mean, self.cov_mat)
        actions = policy_dist.sample()
        return actions, policy_dist.log_prob(actions)
    
    def compute_log_prob(self, actions: torch.Tensor, observation: torch.Tensor) -> torch.Tensor:
        mean =  self.actor(observation) * self.env.get_action_constraints()
        policy_dist = MultivariateNormal(mean, self.cov_mat)
        return policy_dist.log_prob(actions)

    def save(self, suffix: str) -> None:
        actor_path = self.actor_saved_filename + f"_{suffix}.pth"
        critic_path = self.critic_saved_filename + f"_{suffix}.pth"
        torch.save(self.actor, actor_path)
        torch.save(self.critic, critic_path)
        print(f"saved actor at {actor_path}")
        print(f"saved critic at {critic_path}")

    def randomize_initial_state(self) -> None:
        random_state = 2 * (torch.rand(size=(self.env.Dimensions.states_dims,)) - 0.5) * self.env.get_state_constraints()
        self.env.set_state(random_state)
