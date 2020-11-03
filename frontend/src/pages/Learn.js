import React, {useEffect, useState} from 'react';
import {Form, FormGroup, Label, Input, Button, Jumbotron, Container} from 'reactstrap';
import Speech from 'speak-tts';
import './Learn.css';
import ec2Url from '../Utilities';
import socket from '../Socket';

const styles = {
    inputContainer:{
        display: 'flex',
        flexDirection: 'row',
    },
    image:{
        height: '200px',
        width: '200px',
        paddingTop: '3%'
    },
    pageContainer:{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        paddingTop: '3%',
    },
}

let speechPtr = null;

function Learn(props){
    const [renderImage, setRenderImage] = useState(false);
    const [renderLetterForm, setRenderLetterForm] = useState(false);
    const [renderWordList, setRenderWordList] = useState(false);
    const [imagePath, setImagePath] = useState('');
    const [textToSpeak, setTextToSpeak] = useState('');
    const [words, setWords] = useState({});
    const [letters, setLetters] = useState({});
    const [feedback, setFeedback] = useState('');
    const [renderFeedback, setRenderFeedback] = useState(false);
    const [prediction, setPrediction] = useState('');
    const [target, setTarget] = useState('');

    // Set up textToSpeech when page first loads
    useEffect(() => {
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

        socket.on("raspberry pi response", (data) => {
            const raspPred = data["response"]["response"];
            setPrediction(raspPred.toLowerCase());
            console.log(raspPred);
        });

    }, [])

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

    const showLetter = (letter) => {
        setImagePath(letters[letter]);
        setTextToSpeak(letter);
        setRenderImage(true);
    }

    // Get image corresponding to letter inputted
    const handleOnSubmit = (event) =>{
        event.preventDefault();
        if(event.target.userInput.value !== ''){
            var input = event.target.userInput.value.toLowerCase();
            showLetter(input);
            setTarget(input);
            document.getElementById("inputForm").reset();
        }
    }

    const showWord = (word) => {
        setImagePath(words[word]);
        setTextToSpeak(word);
        setRenderImage(true);
    }

    // When a specific word is pressed, show the image and have text to speech say the word
    const handleWordButton = (word) =>{
        showWord(word);
        setTarget(word);
    }

    // Whenever a new image is rendered, textToSpeech occurs
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

    }, [imagePath, textToSpeak])

    // Change layout of page to show letter input form when the letter button is clicked
    // Get letters from server
    const handleShowLetterButtonPress = () =>{
        if(Object.keys(letters).length === 0){
            let url = ec2Url + 'letters';
            fetch(url)
            .then(response => response.json())
            .then(data => setLetters(data));
        }
        setTarget('');
        setRenderLetterForm(true);
        if(renderWordList){
            setRenderWordList(false);
        }
        if(renderImage){
            setRenderImage(false);
        }
        if(renderFeedback){
            setRenderFeedback(false);
        }
    }
 
    // Change layout of page to show word buttons when the word button is clicked
    // Get words from server
    const handleShowWordButtonPress = () => {
        if(Object.keys(words).length === 0){
            let url = ec2Url + 'words';
            fetch(url)
            .then(response => response.json())
            .then(data => setWords(data));
        }
        setTarget('');
        setRenderWordList(true);
        if(renderLetterForm){
            setRenderLetterForm(false);
        }
        if(renderImage){
            setRenderImage(false);
        }
        if(renderFeedback){
            setRenderFeedback(false);
        }
    }

    return(
        <div>
            {renderLetterForm || renderWordList ?
                null
            :
                <Jumbotron fluid>
                    <Container fluid>
                        <h1 className="display-3">Teach Yourself!</h1>
                        <p className="lead">Want to learn some American Sign Language?</p>
                        <p className="lead">Well you're at the right place!</p>
                        <p className="lead">Choose between words and letters to see how they're signed.</p>
                        <p className="lead">Make sure to have your sound on so you can hear each word and letter!</p>
                    </Container>
                </Jumbotron>
            }
            
            <div className="questionContainer">
                <p className="lead">Do you want to learn:</p>
                <div className="choicesContainer">
                    <Button className="wordsButton" onClick={handleShowWordButtonPress}>Words</Button> 
                    <p style={{paddingTop: '5%'}} className="lead">or</p> 
                    <Button onClick={handleShowLetterButtonPress}className="lettersButton">Letters</Button>
                </div>
            </div>
            
            {renderLetterForm ? 
                <div style={styles.pageContainer}>
                <Form onSubmit={handleOnSubmit} id="inputForm">
                    <FormGroup style={{paddingTop: '5%'}}>
                        <Label className="lead" for="userInput">Enter a letter to see what it looks like in American Sign Language</Label>
                        <div style={styles.inputContainer}>
                            <Input 
                                maxLength="1" 
                                type="textArea" 
                                name="input" 
                                id="userInput"
                            />
                            <Button style={{marginLeft: '1%'}}>Submit</Button>
                        </div>
                    </FormGroup>
                </Form>

                {renderFeedback ?
                        feedback === "Correct" ? 
                            <h1 style={{color: "green"}}>Correct</h1>
                        :
                            <h1 style={{color: "red"}}>Incorrect</h1>
                    :
                        null
                }
                
                {renderImage ? 
                    (<img 
                        alt="sign language equivalent"
                        src = {imagePath}
                        style={styles.image} 
                    />)
                :
                    (null)
                }
            </div>
            :
                null
            }

            {renderWordList ? 
                <div className="wordContainer">
                    <p className="lead">Press a button see what the word looks like in American Sign Language</p>
                    <div className="wordButtonContainer">
                            {/* <Button  onClick={(word) => handleWordButton('monday')}className="wordButton">Monday</Button> */}
                            {/* <Button  onClick={(word) => handleWordButton('tuesday')}className="wordButton">Tuesday</Button> */}
                            {/* <Button  onClick={(word) => handleWordButton('wednesday')} className="wordButton">Wednesday</Button> */}
                            {/* <Button  onClick={(word) => handleWordButton('thursday')} className="wordButton">Thursday</Button> */}
                            {/* <Button  onClick={(word) => handleWordButton('friday')} className="wordButton">Friday</Button> */}

                            {/* <Button  onClick={(word) => handleWordButton('saturday')} className="wordButton">Saturday</Button> */}
                            <Button onClick={(word) => handleWordButton('sunday')} className="wordButton">Sunday</Button>
                            <Button onClick={(word) => handleWordButton('hello')} className="wordButton">Hello</Button>

                            <Button onClick={(word) => handleWordButton('thanks')} className="wordButton">Thanks</Button>
                            {/* <Button  onClick={(word) => handleWordButton('goodbye')} className="wordButton">Goodbye</Button> */}
                            {/* <Button  onClick={(word) => handleWordButton('nicetomeetyou')} className="wordButton">Nice to meet you</Button> */}
                    </div>

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
                            alt="sign language equivalent"
                            src={imagePath}
                            style = {styles.image}
                        />
                    :
                        null
                    }
                </div>
            :
                null
            }

        </div>
    );
}

export default Learn;