import React, { useEffect, useState } from 'react';
import {Button, Jumbotron, Container} from 'reactstrap';
import ec2Url from '../Utilities';
import Speech from 'speak-tts';

let speechPtr = null;

function Test(props){
    const [allPaths, setAllPaths] = useState({});
    const [allSigns, setAllSigns] = useState([]);
    const [imagePath, setImagePath] = useState('');
    const [renderImage, setRenderImage] = useState(false);
    const [textToSpeak, setTextToSpeak] = useState('');

    // min, max included
    const getRandomNumber = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);

    useEffect(() => {
        if(Object.keys(allPaths).length === 0){
            let url = process.env.NODE_ENV === 'production' ? ec2Url + 'all' : 'http://localhost:5000/all';
            fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                setAllSigns(data['allSigns']);
                setAllPaths(data['allPaths']);
            })
        }

        const speech = new Speech();

        if(speech.hasBrowserSupport()){ // Check if text to speech is available
            console.log("Speech translation supported");
            speech.init()
            .then((data) => { // Initialize speech object
                console.log("Speech is ready, voices are available", data)
            })
            .catch(e => {
                console.log("An error occurred while initializing: ", e)
            })

            speechPtr = speech; // Assign speechPtr speech so we can use it throughout component
        }
        else{
            console.log("Speech translation not supported");
        }
    }, [allPaths])

    const getRandomSign = () => {
        var randomNum = getRandomNumber(0, Object.keys(allSigns).length - 1);
        var sign = allSigns[randomNum];
        setImagePath(allPaths[sign]);
        setTextToSpeak(sign);
        setRenderImage(true);
    }

    useEffect(() => {
        speechPtr.speak({
            text: textToSpeak
        })
        .then(() => {
            console.log("Success!")
        })
        .catch(e => {
            console.log("An error occurred:", e)
        })

    }, [textToSpeak])

    return(
        <div>
        <Jumbotron fluid>
            <Container fluid>
                <h1 className="display-3">Test Yourself!</h1>
                <p className="lead">Let's see what you've learned.</p>
                <p className="lead">Press the button below to get a random sign!</p>
            </Container>
        </Jumbotron>
 
        <div className="questionContainer">
            <Button onClick={getRandomSign}>Get a random sign</Button>
        </div>

        {renderImage ? 
            <img
                alt="sign language equivalent" 
                src={imagePath} 
            />
        :
            null
        }
    </div>

    );
}

export default Test;