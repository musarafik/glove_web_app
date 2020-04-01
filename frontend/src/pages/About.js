import React from 'react';
import Image from 'react-bootstrap/Image';
import team from '../assets/team.png';

// export const About  = () =>(
const About = () =>(
    <div>
        <h2>About Page</h2>
        <Image src={team} fluid/>
    </div>
)

export default About;
