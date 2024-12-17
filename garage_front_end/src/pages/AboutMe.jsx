import './page.css'
import thinker from "../images/thinker.jpg"
let AboutMe = () => {
    return (<div>
        <h2>About me</h2>
        <img src={thinker} alt="Thinker" class="image-resized"></img>
        <hr />
        <p className="p">
            I am a robotics software engineer with a passion for motion planning, dynamical systems, controls and reinforcement learning.
            <br></br>
            Based in Zurich Switzerland, originally from Kalamata, Greece.
        </p>
        <a className='link-style' href="CV.pdf" target="_blank" download>Download CV</a>
        <a className='link-style' href="https://www.linkedin.com/in/panagiotis-anagnostaras-1aa7b5155/" target="_blank">Linkedin account</a>
    </div>)
}

export default AboutMe;