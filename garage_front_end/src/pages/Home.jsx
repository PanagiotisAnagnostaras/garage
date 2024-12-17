import { Link } from 'react-router-dom';
import './Home.css'
let Home = () => {
    return (<header className="App-header">
        <h1 className='h1'>Welcome to my garage</h1>
        <Link to="aboutme"  className="link-style">About me</Link>
        <Link to="projects" className='link-style'>Some projects</Link>
        <a className='link-style' href="https://github.com/PanagiotisAnagnostaras/garage" target="_blank">GitHub Repo</a>
    </header>)
};

export default Home;