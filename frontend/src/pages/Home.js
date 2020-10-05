import React from 'react';

const Home  = () =>(
    <div>
      <div class="jumbotron">
        <h1>Team I4: Sign Language Translator Glove</h1>
        <img src={require('../assets/gl.png')} height="100" width="100" alt="logo"></img> 
      </div>
        <div class="jumbotron">
          <h2>Our Goal...</h2>
          <p>To design a glove capable of translating sign language in real time. We are designing this glove to help people learn sign language by creating an environment where users can test their sign language wherever they can use electronics.</p>
        
          <h2>The Design Problem</h2>
          <p>The goal of this project is to create a portable glove that accurately translates sign language and have this translation available in real-time through a website. This glove will help people learn sign language by creating an environment where users can practice their signing almost anywhere and receive accurate feedback in real-time. Due to the approximately 466 million people in the world with hearing disabilities, it is paramount that people learn sign language to be able to communicate with this large portion of the population. Currently, there is a lack of supplemental services and tools to help people learn sign language, and we believe our glove can help satisfy this need.</p>
        </div>
        
        
        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gridGap: 20 }}>
          <div>
            <p style={{fontWeight: 'bold'}}> Our Connections</p>
            <div><img src={require('../assets/connections.png')} height = "512" width = "384" alt=""/></div>   
          </div>
          <div>
            <p style={{fontWeight: 'bold'}}> Prototype Glove</p>
            <div><img src={require('../assets/bglove.png')} alt=""/></div>
          </div>
          <p></p>
        </div>

        <div class="jumbotron">
            <h2>Specifications</h2>
            <p>In order to measure the success of our glove serving as such a tool, we have laid out the following parameters for the project’s success: </p>
            <ul>
                <li>The algorithm must be able to accurately translate user input from the glove.</li>
                <li>The algorithm needs to be fast in order to produce an output on the website in close to real time.</li>
                <li>The website needs to be easily navigable as well as have a user-friendly and intuitive interface.</li>
                <li>The glove needs to be able to produce consistent sensor readings.</li>
                <li>The glove needs to be portable and lightweight.</li>
            </ul>
        </div>
        <p></p>
        <div class="jumbotron">
            <h2>Design Solution</h2>
            <p>The project is divided into three subsystems - the glove, Raspberry Pi Zero and website. The glove is composed of various sensors that take in data from the user’s gestures. Then, data from the glove is processed in the Raspberry Pi Zero running a support vector machine (SVM) algorithm to determine the sign. Finally, the translation determined by the algorithm is outputted to the website where the user can see the result of their signing. Figure 1 below demonstrates the three subsystems and flow of data through each component.</p>
            <div style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
                <img src={require('../assets/blockd.png')} alt=""/>
            </div>
            <h5>The Glove</h5>
            <p>The glove interacts with all the other facets of the project by handling the user sign language input and outputs sensor reading information. The output is sent to the attached Raspberry Pi Zero that is connected to the glove through a printed circuit board (PCB). Each sensor sends different information to the Raspberry Pi Zero: the flex sensors detect how much each finger is bent, the inertial measurement unit (IMU) detects the position and angle of the hand, and the force sensors detect if the fingers are crossed or pressed together. Once the readings are sent to the next subsystem, the glove continues to read the sensors for new information. </p>
            <h5>The Raspberry Pi</h5>
            <p>The Raspberry Pi receives input from the glove in the form of the flex sensor readings and outputs the translation of what the user is signing. The Raspberry Pi can accomplish this through the support vector machine (SVM) algorithm that will be running inside. The algorithm will be trained and tested on a large data set of sensor readings we record from our glove, so it will filter out noise and will give predictions knowing the range of values each sensor will have based on the input. </p>
            <h5>The Website</h5>
            <p>The website receives input from the Raspberry Pi Zero in the form of the translated sign language and outputs the translation to the user in the form of displaying the translation, so that they can see how accurately they were signing. The website gives the option of outputting the translation with text on the screen or using text-to-speech to give people the opportunity to learn in whichever way benefits them the best. Another output that the website has which benefits the user’s learning experience is showing the user how to sign specific words by pressing a button. The website’s output finishes the system’s cycle.</p>
        </div>
        <p></p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gridGap: 20 }}>
          <div>
            <p style={{fontWeight: 'bold'}}> Diagram of Connections</p>
            <div><img src={require('../assets/con_diagram.png')} height = "512" width = "384" alt=""/></div>   
          </div>
          <div>
            <p style={{fontWeight: 'bold'}}> Fritzing Design</p>
            <div><img src={require('../assets/fritzing.png')} height = "512" width = "384" alt=""/></div>
          </div>
          <p></p>
        </div>
        <p></p>
        <div class="jumbotron">
            <h2>Alternate Designs</h2>
            <p>We have considered alternate designs for the machine learning algorithm and website. In terms of the algorithm, we have also tested a linear regression algorithm to see its performance on sample data. Linear regression is a simpler algorithm to implement, but we found it to be less accurate than the SVM algorithm. As a result, we have decided to implement the SVM algorithm in our overall glove design. In regards to the website, we have considered having a single page that translates input from the glove, rather than having a learning and testing section. However, we decided to progress with the later choice because it is more inline with our purpose of creating an educational tool. </p>
        </div>
    </div>
)

export default Home;
