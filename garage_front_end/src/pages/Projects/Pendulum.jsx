import '../page.css';
import pendulum from "../../images/pendulum.png";
import React, { useState } from 'react';

let Pendulum = () => {
    const [simSteps, setSimSteps] = useState("");
    const [intTimeStep, setIntTimeStep] = useState("");
    const [pendPos, setPendPos] = useState("");
    const [pendVel, setPendVel] = useState("");
    const [responseData, setResponseData] = useState("");
    const [successfulPost, setSuccessfulPost] = useState(true);

    const sendData = async () => {
        const data = { "simulation_steps": simSteps, "integration_time_step": intTimeStep, "pendulum_position" : pendPos, "pendulum_velocity": pendVel};
        console.log(data)
        try {
            const response = await fetch('http://localhost:4000/api/v1/simulation/', {
                method: 'POST',
                headers: {
                    'HOST': 'frontend',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.text();
            console.log(JSON.parse(result));
            setResponseData(JSON.parse(result));
            setSuccessfulPost(true)
        } catch (error) {
            console.error('Error sending data:', error);
            setSuccessfulPost(false);
        }
    };

    return (
        <div>
            <h2>Inverted Pendulum</h2>
            <a className='link-style' href="https://github.com/PanagiotisAnagnostaras/garage/tree/master/projects/inverted_pendulum" target="_blank" rel="noopener noreferrer">Code</a>
            <p>This project is about simulating a cart-pendulum system in C++.</p>
            <img src={pendulum} alt="pendulum"></img>
            <h3>Simulation Data</h3>
            <div className="input-container">
                <div className="input-item">
                    <label htmlFor="input1" className="input-label">Number of simulation steps</label>
                    <input
                        id="input1"
                        type="text"
                        value={simSteps}
                        onChange={(e) => setSimSteps(e.target.value)}
                        placeholder="int"
                        className="input-field"
                    />
                </div>
                <div className="input-item">
                    <label htmlFor="input2" className="input-label">Integration time step [sec]</label>
                    <input
                        id="input2"
                        type="text"
                        value={intTimeStep}
                        onChange={(e) => setIntTimeStep(e.target.value)}
                        placeholder="float"
                        className="input-field"
                    />
                </div>
                <div className="input-item">
                    <label htmlFor="input3" className="input-label">Initial angle of pendulum [deg]</label>
                    <input
                        id="input3"
                        type="text"
                        value={pendPos}
                        onChange={(e) => setPendPos(e.target.value)}
                        placeholder="float"
                        className="input-field"
                    />
                </div>
                <div className="input-item">
                    <label htmlFor="input4" className="input-label">Initial angular velocity of pendulum [deg/sec]</label>
                    <input
                        id="input4"
                        type="text"
                        value={pendVel}
                        onChange={(e) => setPendVel(e.target.value)}
                        placeholder="float"
                        className="input-field"
                    />
                </div>
                <button onClick={sendData}>Start</button>
            </div>
            {successfulPost && responseData && <div><h4>Started simulation</h4></div>}
            {!successfulPost && <div><h4>Failed to start simulation. Check your inputs.</h4></div>}
        </div>
    );
};

export default Pendulum;
