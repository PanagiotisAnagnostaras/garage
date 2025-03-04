import torch.torch_version
from networks import Actor, Critic
import torch
from env import Env
from torch.distributions import MultivariateNormal
from utils import plot_rollout
from datetime import datetime


class PPO:
    def __init__(self, env, steps_per_rollout, n_epochs_per_training_step, n_rollouts_per_training_step, lr_actor, lr_critic, epsilon) -> None:
        current_datetime = datetime.now()
        current_datetime_str = current_datetime.strftime("%Y_%m_%d_%H_%M")
        self.env: Env = env
        self._init_hyperparameters(steps_per_rollout=steps_per_rollout, n_epochs_per_training_step=n_epochs_per_training_step, n_rollouts_per_training_step=n_rollouts_per_training_step, lr_actor=lr_actor, lr_critic=lr_critic, epsilon=epsilon)
        self.actor = Actor(self.env.dimensions.observations_dims, self.env.dimensions.actions_dims)
        self.actor_opt = torch.optim.Adam(self.actor.parameters(), lr=self.lr_actor)
        self.actor_saved_filename = f"/garage_back_end/projects/ppo/saved_models/{current_datetime_str}_saved_actor"
        self.critic = Critic(self.env.dimensions.observations_dims)
        self.critic_opt = torch.optim.SGD(self.critic.parameters(), lr=self.lr_critic)
        self.critic_saved_filename = f"/garage_back_end/projects/ppo/saved_models/{current_datetime_str}_saved_critic"

    def _init_hyperparameters(self, steps_per_rollout, n_epochs_per_training_step, n_rollouts_per_training_step, lr_actor, lr_critic, epsilon) -> None:
        self.steps_per_rollout = steps_per_rollout
        self.gamma = 0.95
        self.lambd = 0.5
        self.n_epochs_per_training_step = n_epochs_per_training_step
        self.n_rollouts_per_training_step = n_rollouts_per_training_step
        self.epsilon = epsilon
        self.lr_actor = lr_actor
        self.lr_critic = lr_critic
        cov_var = torch.full(size=(self.env.dimensions.actions_dims,), fill_value=5.0)
        self.cov_mat = torch.diag(cov_var)

    def train(self, total_training_steps):
        step = 0
        while step < total_training_steps:
            print(f"-------------- training steps = {step+1}/{total_training_steps} --------------")
            obs_buffer = torch.zeros(size=(self.n_rollouts_per_training_step, self.steps_per_rollout + 1, self.env.dimensions.observations_dims))
            acts_buffer = torch.zeros(size=(self.n_rollouts_per_training_step, self.steps_per_rollout, self.env.dimensions.actions_dims))
            rews_buffer = torch.zeros(size=(self.n_rollouts_per_training_step, self.steps_per_rollout, 1))
            log_prob_buffer = torch.zeros(size=(self.n_rollouts_per_training_step, self.steps_per_rollout, 1))
            for rollout in range(self.n_rollouts_per_training_step):
                # print(f"rollout {rollout+1}/{self.n_rollouts_per_training_step}")
                obs, acts, rews, log_prob = self.rollout()
                # plot_rollout(obs)
                obs_buffer[rollout, :, :] = obs
                acts_buffer[rollout, :, :] = acts
                rews_buffer[rollout, :, :] = rews.unsqueeze(-1)
                log_prob_buffer[rollout, :, :] = log_prob.unsqueeze(-1)

            print(f"avg reward per rollout = {rews_buffer.sum()/self.n_rollouts_per_training_step} mean action = {acts_buffer.sum()/acts_buffer.nelement()}")
            advantages_buffer, rews2go_buffer = self.compute_advantages_and_rews2go(rews_buffer=rews_buffer, obs_buffer=obs_buffer)
            for epoch in range(self.n_epochs_per_training_step):
                actor_loss = self.update_actor(log_prob_before_buffer=log_prob_buffer, obs_buffer=obs_buffer, advantages_buffer=advantages_buffer)
                critic_loss = self.update_critic(obs_buffer=obs_buffer, rews2go_buffer=rews2go_buffer)
                print(f"epoch: {epoch}/{self.n_epochs_per_training_step} actor loss = {actor_loss} critic loss = {critic_loss}")
            if step % 2 == 0:
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
        for step in range(self.steps_per_rollout):
            a, log_prob = self.compute_actions(s)
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
        for step in reversed(range(self.steps_per_rollout)):
            # print(f"step={step}")
            next_observation = obs_buffer[:, step + 1, :]
            observation = obs_buffer[:, step, :]
            delta = rews_buffer[:, step, :] + self.gamma * self.read_value_function(next_observation) - self.read_value_function(observation)  # to check again
            advantage = delta + (self.gamma * self.lambd) * advantages[:, 0, :] if len(advantages) != 0 else delta
            advantage = advantage.unsqueeze(1)
            advantages = torch.cat((advantage, advantages), dim=1) if advantages.nelement() != 0 else advantage
            rew2go = rews_buffer[:, step, :] + self.gamma * (rews2go[:, 0, :]) if len(rews2go) != 0 else rews_buffer[:, step, :]
            rew2go = rew2go.unsqueeze(1)
            rews2go = torch.cat((rew2go, rews2go), dim=1) if rews2go.nelement() != 0 else rew2go
        # normalize advantage to do
        return advantages, rews2go

    def update_actor(self, log_prob_before_buffer: torch.Tensor, obs_buffer: torch.Tensor, advantages_buffer: torch.Tensor) -> None:
        _, log_prob = self.compute_actions(obs=obs_buffer[:, :-1, :])
        ratio = torch.exp(log_prob - log_prob_before_buffer.detach().squeeze())
        surr_clipped = torch.clamp(ratio, 1 - self.epsilon, 1 + self.epsilon) * advantages_buffer.detach().squeeze()
        surr_unclipped = ratio * advantages_buffer.detach().squeeze()
        actor_loss = -torch.min(surr_clipped, surr_unclipped).mean()
        self.actor_opt.zero_grad()
        actor_loss.backward()
        self.actor_opt.step()
        return actor_loss.item()

    def update_critic(self, obs_buffer: torch.Tensor, rews2go_buffer: torch.Tensor) -> None:
        predicted_V = self.read_value_function(obs=obs_buffer[:, :-1, :])
        critic_loss: torch.Tensor = torch.nn.MSELoss()(predicted_V, rews2go_buffer.detach())
        self.critic_opt.zero_grad()
        critic_loss.backward()
        self.critic_opt.step()
        return critic_loss.item()

    def read_value_function(self, obs: torch.Tensor) -> float:
        return self.critic(obs)

    def compute_actions(self, obs: torch.Tensor) -> torch.Tensor:
        mean = self.actor(obs) * self.env.constraints.max_input
        dist = MultivariateNormal(mean, self.cov_mat)
        action = dist.sample()
        # print(f"mean={mean} actions={action}")
        log_prob = dist.log_prob(action)
        return action, log_prob

    def save(self, suffix: str) -> None:
        torch.save(self.actor, self.actor_saved_filename + f"_{suffix}.pth")
        torch.save(self.critic, self.critic_saved_filename + f"_{suffix}.pth")

    def randomize_initial_state(self) -> None:
        cart_vel = (torch.rand(size=(1,)) * 2 - 1) * self.env.constraints.max_cart_vel
        pend_vel = (torch.rand(size=(1,)) * 2 - 1) * self.env.constraints.max_pend_vel
        pend_pos = (torch.rand(size=(1,))) * 2 * torch.pi
        self.env.set_state(cart_vel=cart_vel.item(), pend_vel=pend_vel.item(), pend_pos=pend_pos.item())
