import '../page.css';
import pendulum from "../../images/pendulum.png";
import React, { useState } from 'react';

let Pendulum = () => {
    const [simData, setSimData] = useState("");
    const [responseData, setResponseData] = useState("");
    const [successfulPost, setSuccessfulPost] = useState(true);

    const sendData = async () => {
        const data = { "simulation_steps": simData };
        console.log(data);
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
            <h3>Run Simulation</h3>
            <input
                type="text"
                value={simData}
                onChange={(e) => setSimData(e.target.value)}
                placeholder="Enter your sim data"
            />
            <button onClick={sendData}>POST</button>
            {successfulPost && responseData && <div><h4>Started simulation with {JSON.stringify(responseData.simulation_steps, null, 2)} steps</h4></div>}
            {!successfulPost && <div><h4>Failed to start simulation. Check your inputs.</h4></div>}
        </div>
    );
};

export default Pendulum;
