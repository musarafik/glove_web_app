import React from 'react';
import {Form, FormGroup, Label, Input, Button, Jumbotron, Container} from 'reactstrap';
import Speech from 'speak-tts';
import './Translator.css';

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


export default class Translator extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            renderImage: false,
            renderLetterForm: false,
            renderWordList: false,
            image: '',
            textToSpeak: '',
            wordCollection: []
        }
    }

    componentDidMount = () =>{
        const speech = new Speech();

        if(speech.hasBrowserSupport()){ // Check if text to speech is available
            console.log("speech translation supported");
            speech.init().then((data) =>{ // Initialize speech object
                console.log("Speech is ready, voices are available", data)
            }).catch(e =>{
                console.log("An error occurred while initializing: ", e)
            })

            speechPtr = speech; // Assign speechPtr speech so we can use it throughout component
        }
        else{
            console.log("Speech translation not supported");
        }
    }

    // Send response to backend in json form with POST request whenever form is submitted
    handleOnSubmit = (event) =>{
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
                this.handleResponse(data);
                this.chooseImage();
                document.getElementById("inputForm").reset();
                speechPtr.speak({
                    text: this.state.textToSpeak,
                }).then(() =>{
                    console.log("Success!")
                }).catch(e =>{
                    console.log("An error occurred:", e)
                })
            });
        }
    }

    // Set image to corresponding response from backend and allow it to be rendered
    handleResponse = (data) =>{
        this.setState({image: data['response']});
        this.setState({renderImage: true});
    }

    // Choose image to render based off backend response
    // Looks up the value of image in letters object
    // Sets what should be spoken by text to speech
    chooseImage = () =>{
        this.setState({image: letters[this.state.image], textToSpeak: this.state.image});
    }

    // When a specific word is pressed, show the image and have text to speech say the word
    handleWordButton = async (word) =>{
        await this.setState({image: words[word], textToSpeak: word});
        this.setState({renderImage: true});
        speechPtr.speak({
            text: this.state.textToSpeak,
        }).then(() =>{
            console.log("Success!")
        }).catch(e =>{
            console.log("An error occurred:", e)
        })
    }

    // Change layout of page to show letter input form when the letter button is clicked
    handleLetterPress = () =>{
        this.setState({renderLetterForm: true});
        if(this.state.renderWordList){
            this.setState({renderWordList: false});
        }
        if(this.state.renderImage){
            this.setState({renderImage: false});
        }
    }
 
    // Change layout of page to show word buttons when the word button is clicked
    handleWordPress = () =>{
        this.setState({renderWordList: true});
        if(this.state.renderLetterForm){
            this.setState({renderLetterForm: false});
        }
        if(this.state.renderImage){
            this.setState({renderImage: false});
        }
    }

    render(){
        return(
            <div>
                {this.state.renderLetterForm || this.state.renderWordList ?
                    null
                :
                    <Jumbotron fluid>
                        <Container fluid>
                            <h1 className="display-3">Translator</h1>
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
                        <Button className="wordsButton" onClick={this.handleWordPress}>Words</Button> 
                        <p style={{paddingTop: '5%'}} className="lead">or</p> 
                        <Button onClick={this.handleLetterPress}className="lettersButton">Letters</Button>
                    </div>
                </div>
               
                {this.state.renderLetterForm ? 
                    <div style={styles.pageContainer}>
                    <Form onSubmit={this.handleOnSubmit} id="inputForm">
                        <FormGroup style={{paddingTop: '5%'}}>
                            <Label className="lead" for="userInput">Enter a letter to see what it looks like in American Sign Language</Label>
                            <div style={styles.inputContainer}>
                                <Input type="textArea" name="input" id="userInput" />
                                <Button style={{marginLeft: '1%'}}>Submit</Button>
                            </div>
                        </FormGroup>
                    </Form>
                    
                    {this.state.renderImage ? 
                        (<img 
                            alt="sign language equivalent"
                            src={this.state.image} 
                            style={styles.image} 
                        />)
                    :
                        (null)
                    }
                </div>
                :
                    null
                }

                {this.state.renderWordList ? 
                    <div className="wordContainer">
                        <p className="lead">Press a button see what the word looks like in American Sign Language</p>
                        <div className="wordButtonContainer">
                                <Button  onClick={(word) => this.handleWordButton('Monday')}className="wordButton">Monday</Button>
                                <Button  onClick={(word) => this.handleWordButton('Tuesday')}className="wordButton">Tuesday</Button>
                                <Button  onClick={(word) => this.handleWordButton('Wednesday')} className="wordButton">Wednesday</Button>
                                <Button  onClick={(word) => this.handleWordButton('Thursday')} className="wordButton">Thursday</Button>
                                <Button  onClick={(word) => this.handleWordButton('Friday')} className="wordButton">Friday</Button>

                                <Button  onClick={(word) => this.handleWordButton('Saturday')} className="wordButton">Saturday</Button>
                                <Button  onClick={(word) => this.handleWordButton('Sunday')} className="wordButton">Sunday</Button>
                                <Button  onClick={(word) => this.handleWordButton('Hello')} className="wordButton">Hello</Button>
                                <Button  onClick={(word) => this.handleWordButton('Goodbye')} className="wordButton">Goodbye</Button>
                                <Button  onClick={(word) => this.handleWordButton('Nice to meet you')} className="wordButton">Nice to meet you</Button>
                        </div>

                            {this.state.renderImage ? 
                                <img 
                                    alt="sign language equivalent"
                                    src={this.state.image}
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
}