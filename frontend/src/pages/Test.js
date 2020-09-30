import React, { useEffect, useState } from 'react';
import {Button, Jumbotron, Container} from 'reactstrap';
import ec2Url from '../Utilities';
import Speech from 'speak-tts';
import socket from '../Socket';

let speechPtr = null;

function Test(props){
    const [allPaths, setAllPaths] = useState({});
    const [allSigns, setAllSigns] = useState([]);
    const [imagePath, setImagePath] = useState('');
    const [renderImage, setRenderImage] = useState(false);
    const [textToSpeak, setTextToSpeak] = useState('');
    const [english, setEnglish] = useState('');
    const [renderEnglish, setRenderEnglish] = useState(false);

    // min, max included
    const getRandomNumber = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);

    useEffect(() => {
        // get S3 paths for images from backend
        if(Object.keys(allPaths).length === 0){
            let url = ec2Url + 'all';
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

        socket.on("raspberry pi response", (data) => console.log(data));
    }, [allPaths])

    const getRandomSign = () => { // 1. press button and get english that user must sign
                                  // 2. then after a delay image of sign is shown
                                  // TODO: add in feedback, make delay work with glove
        var randomNum = getRandomNumber(0, Object.keys(allSigns).length - 1);
        var sign = allSigns[randomNum];
        setEnglish(sign);
        setRenderEnglish(true);
        setImagePath(allPaths[sign]);
        setTextToSpeak(sign);
        setTimeout(function(){setRenderImage(true);}, 3000);
        setTimeout(function(){}, 3000);
        setRenderImage(false);
        
        socket.emit("send_message", "sending message to server");
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

        {renderEnglish ? 
            <h1>{english}</h1>
        :
            null
        }

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