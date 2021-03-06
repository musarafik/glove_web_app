import React, { useEffect, useState } from 'react';
import {Button, Jumbotron, Container} from 'reactstrap';
import ec2Url from '../Utilities';
import Speech from 'speak-tts';
import socket from '../Socket';
import './Test.css';

let speechPtr = null;

function Test(props){
    const [allPaths, setAllPaths] = useState({}); 
    const [allSigns, setAllSigns] = useState([]);
    const [imagePath, setImagePath] = useState('');
    const [renderImage, setRenderImage] = useState(false);
    const [textToSpeak, setTextToSpeak] = useState('');
    const [target, setTarget] = useState('');
    const [renderTarget, setRenderTarget] = useState(false);
    const [feedback, setFeedback] = useState('');
    const [renderFeedback, setRenderFeedback] = useState(false);
    const [prediction, setPrediction] = useState('');

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

        // Set up text to speech
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

        // Listen for predictions from Raspberry Pi
        socket.on("raspberry pi response", (data) => {
            const raspPred = data["response"]["response"];
            setPrediction(raspPred.toLowerCase());
            console.log(raspPred);
            setTimeout(function(){setPrediction('');}, 1000);
        });
    }, [allPaths])

    const handleButtonClick = () => { 
        var sign = getRandomSign();
        showTarget(sign);    
    }

    // Get a random target sign for the user to make
    // Returns the English text 
    const getRandomSign = () => {
        var randomNum = getRandomNumber(0, Object.keys(allSigns).length - 1);
        return allSigns[randomNum];
    }

    // Display the target sign the user needs to make
    const showTarget = (sign) => {
        setTarget(sign);
        setRenderTarget(true);
    }

    // When prediction changes call this
    // Compare prediction with the target and set feedback to Correct if they are the same, otherwise Incorrect
    useEffect(() => {
        if(prediction !== '' && target !== ''){
            setTimeout(function(){setRenderFeedback(true);}, 1000);
            if(prediction === target){
                setFeedback("Correct");
            }
            else{
                setFeedback("Incorrect");
            }
            setRenderFeedback(false);
        }  
    }, [prediction])

    // Whenever target word changes this is called to show how the sign is formed
    useEffect(() => {
        if(target !== ''){
            setImagePath(allPaths[target]);
            setTextToSpeak(target);
            setTimeout(function(){setRenderImage(true);}, 1000);
            setRenderImage(false);
        }
    }, [target])

    // Do text to speech after the sign that needs to be spoken is set
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
            <Button onClick={handleButtonClick}>Get a random sign</Button>
        </div>

        <div className="feedbackContainer">
            {renderTarget ? 
                <h1>{target}</h1>
            :
                null
            }

            {renderFeedback ? 
                feedback === "Correct" ? 
                    <h1 style={{color: "green"}}>Correct</h1>
                :
                    <h1 style={{color: "red"}}>Incorrect</h1>
            :   
                null 
            }

            {renderImage ? 
                <img
                    style={{height: 200, width: 200}}
                    alt="sign language equivalent" 
                    src={imagePath} 
                />
            :
                null
            }
        </div>
    </div>

    );
}

export default Test;