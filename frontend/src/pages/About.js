import React from 'react';
import Table from 'react-bootstrap/Table'

// export const About  = () =>(
const About = () =>(
    <div>
        <h2>About Us</h2>
        <div></div>
        <Table striped bordered hover variant="dark">
            <thead>
                <tr>
                <th>#</th>
                <th>Name</th>
                <th>Planned Contributions</th>
                <th>Areas of Expertise</th>
                <th>Related Coursework</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                <td>1</td>
                <td>Tania Cintron</td>
                <td>Support Vector Machine Algorithm</td>
                <td>Python, Data Science, Machine Learning</td>
                <td>Digital Image Processing, Data Science Principle, Data Science Lab</td>
                </tr>
                <tr>
                <td>2</td>
                <td>Morgan Murrell</td>
                <td>Glove Setup (Raspberry Pi, PCB Planning), Project Organization</td>
                <td>Writing Software, Java, Python, Embedded Systems Programming (C)</td>
                <td>Embedded Systems Design Lab, Digital Logic Design</td>
                </tr>
                <tr>
                <td>3</td>
                <td>Ankur Kaushik</td>
                <td>Web Design/Development</td>
                <td>Writing Software, Java, Web Development, React, Bootstrap, HTML, CSS</td>
                <td>Software Lab, Software Design and Implementation, Software Testing</td>
                </tr>
                <tr>
                <td>4</td>
                <td>Musa Rafik</td>
                <td>Web Design/Development</td>
                <td>Writing Software, Java, Web Development, Node, React, Bootstrap, HTML, CSS, Python, Flask</td>
                <td>Data Science Lab, Software Testing</td>
                </tr><tr>
                <td>5</td>
                <td>Jason Zhang</td>
                <td>Glove Setup (Sensor Setup and ADC)</td>
                <td>Embedded Systems Programming (C), Python</td>
                <td>Embedded Systems Design Lab</td>
                </tr><tr>
                <td>6</td>
                <td>Lucas Best</td>
                <td>Glove Setup (Raspberry Pi, Sensor Setup), Sensor Data Collection</td>
                <td>Writing Software, Embedded Systems (C), Java</td>
                <td>Software Lab, Digital Logic Design</td>
                </tr>
            </tbody>
            </Table>
    </div>
)

export default About;
