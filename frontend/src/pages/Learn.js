import React, {useEffect, useState} from 'react';
import {Form, FormGroup, Label, Input, Button, Jumbotron, Container} from 'reactstrap';
import Speech from 'speak-tts';
import './Learn.css';

// Images for translation
import a from '../assets/a.png';
import b from '../assets/b.jpg';
import c from '../assets/c.jpg';
import d from '../assets/d.jpg';
import e from '../assets/e.png';
import f from '../assets/f.jpg';
import g from '../assets/g.jpg';
import h from '../assets/h.jpg';
import i from '../assets/i.png';
import j from '../assets/j.png';
import k from '../assets/k.png';
import l from '../assets/l.jpg';
import m from '../assets/m.png';
import n from '../assets/n.png';
import o from '../assets/o.png';
import p from '../assets/p.png';
import q from '../assets/q.png';
import r from '../assets/r.png';
import s from '../assets/s.png';
import t from '../assets/t.png';
import u from '../assets/u.png';
import v from '../assets/v.png';
import w from '../assets/w.png';
import x from '../assets/x.png';
import y from '../assets/y.jpg';
import z from '../assets/z.png';

// Words for translation
import monday from '../assets/monday.jpg';
import tuesday from '../assets/tuesday.jpg';
import wednesday from '../assets/wednesday.jpg';
import thursday from '../assets/thursday.jpg';
import friday from '../assets/friday.jpg';
import saturday from '../assets/saturday.jpg';
import sunday from '../assets/sunday.jpg';
import hello from '../assets/hello.jpg';
import goodbye from '../assets/goodbye.jpg';
import nicetomeetyou from '../assets/nicetomeetyou.jpg';


const styles = {
    inputContainer:{
        display: 'flex',
        flexDirection: 'row',
    },
    image:{
        height: '300px',
        width: '300px',
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

const letters = {
    'a': a,
    'b': b,
    'c': c,
    'd': d,
    'e': e,
    'f': f,
    'g': g,
    'h': h,
    'i': i,
    'j': j,
    'k': k,
    'l': l,
    'm': m,
    'n': n,
    'o': o,
    'p': p,
    'q': q,
    'r': r,
    's': s,
    't': t,
    'u': u,
    'v': v,
    'w': w,
    'x': x,
    'y': y,
    'z': z
}

const words = {
    'Monday': monday,
    'Tuesday': tuesday,
    'Wednesday': wednesday,
    'Thursday': thursday,
    'Friday': friday,
    'Saturday': saturday,
    'Sunday': sunday,
    'Hello': hello,
    'Goodbye': goodbye,
    'Nice to meet you': nicetomeetyou
}


function Learn(props){
    const [renderImage, setRenderImage] = useState(false);
    const [renderLetterForm, setRenderLetterForm] = useState(false);
    const [renderWordList, setRenderWordList] = useState(false);
    const [image, setImage] = useState('');
    const [imagePath, setImagePath] = useState('');
    const [textToSpeak, setTextToSpeak] = useState('');

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
    }, [])

    // Send response to backend in json form with POST request whenever form is submitted
    const handleOnSubmit = (event) =>{
        event.preventDefault();
        if(event.target.userInput.value !== ''){
            fetch('http://ec2-18-217-92-92.us-east-2.compute.amazonaws.com/translator', { 
                method: 'POST',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(event.target.userInput.value)
            })
            .then(response => response.json())
            .then(data => {
                handleResponse(data);
                chooseImage();
                document.getElementById("inputForm").reset();
                speechPtr.speak({
                    text: textToSpeak
                }).then(() =>{
                    console.log("Success!")
                }).catch(e =>{
                    console.log("An error occurred:", e)
                })
            });
        }
    }

    // Set image to corresponding response from backend and allow it to be rendered
    const handleResponse = (data) => {
        setImagePath(data['response']);
        setRenderImage(true);
    }

    // Choose image to render based off backend response
    // Looks up the value of image in letters object
    // Sets what should be spoken by text to speech
    const chooseImage = () =>{
        setImage(letters[imagePath]);
        console.log(image);
        setTextToSpeak(imagePath);
        // this.setState({image: letters[this.state.image], textToSpeak: this.state.image});
    }

    useEffect(() => {
        speechPtr.speak({
            text: textToSpeak
        })
        .then(() => {
            console.log("Success!")
        })
        .catch(e => {
            console.log("An error occurred:", e);
        })
    }, [image])

    // When a specific word is pressed, show the image and have text to speech say the word
    const handleWordButton = (word) =>{
        setImage(words[word]);
        setTextToSpeak(word);
        setRenderImage(true);
    }

    // Change layout of page to show letter input form when the letter button is clicked
    const handleShowLetterButtonPress = () =>{
        setRenderLetterForm(true);
        // this.setState({renderLetterForm: true});
        if(renderWordList){
            setRenderWordList(false);
        }
        if(renderImage){
            setRenderImage(false);
        }
    }
 
    // Change layout of page to show word buttons when the word button is clicked
    const handleShowWordButtonPress = () =>{
        setRenderWordList(true);
        if(renderLetterForm){
            setRenderLetterForm(false);
        }
        if(renderImage){
            setRenderImage(false);
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
                            <Input type="textArea" name="input" id="userInput" />
                            <Button style={{marginLeft: '1%'}}>Submit</Button>
                        </div>
                    </FormGroup>
                </Form>
                
                {renderImage ? 
                    (<img 
                        alt="sign language equivalent"
                        src = {image}
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
                            <Button  onClick={(word) => handleWordButton('Monday')}className="wordButton">Monday</Button>
                            <Button  onClick={(word) => handleWordButton('Tuesday')}className="wordButton">Tuesday</Button>
                            <Button  onClick={(word) => handleWordButton('Wednesday')} className="wordButton">Wednesday</Button>
                            <Button  onClick={(word) => handleWordButton('Thursday')} className="wordButton">Thursday</Button>
                            <Button  onClick={(word) => handleWordButton('Friday')} className="wordButton">Friday</Button>

                            <Button  onClick={(word) => handleWordButton('Saturday')} className="wordButton">Saturday</Button>
                            <Button  onClick={(word) => handleWordButton('Sunday')} className="wordButton">Sunday</Button>
                            <Button  onClick={(word) => handleWordButton('Hello')} className="wordButton">Hello</Button>
                            <Button  onClick={(word) => handleWordButton('Goodbye')} className="wordButton">Goodbye</Button>
                            <Button  onClick={(word) => handleWordButton('Nice to meet you')} className="wordButton">Nice to meet you</Button>
                    </div>

                        {renderImage ? 
                            <img 
                                alt="sign language equivalent"
                                src={image}
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