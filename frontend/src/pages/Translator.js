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


const styles = {
    inputContainer:{
        display: 'flex',
        flexDirection: 'row',
    },
    image:{
        height: '300px',
        width: '300px',
        paddingTop: '10%'
    },
    pageContainer:{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        paddingTop: '3%'
    },
}

let speechPtr = null; 


export default class Translator extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            renderImage: false,
            renderLetterForm: false,
            renderWordList: false,
            image: '',
            textToSpeak: ''
        }
    }

    componentDidMount = () =>{
        const speech = new Speech();

        if(speech.hasBrowserSupport()){
            console.log("speech translation supported");
            speech.init().then((data) =>{
                console.log("Speech is ready, voices are available", data)
            }).catch(e =>{
                console.log("An error occurred while initializing: ", e)
            })

            speechPtr = speech;
        }
        else{
            console.log("Speech translation not supported");
        }
    }

    // Send response to backend in json form with POST request whenever form is submitted
    handleOnSubmit = (event) =>{
        event.preventDefault();
        if(event.target.userInput.value !== ''){
            fetch('/translator', { 
                method: 'POST',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(event.target.userInput.value)
            })
            .then(response => response.json())
            .then(data => {
                this.handleImage(data);
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

    handleImage = (data) =>{
        this.setState({image: data['response']});
        this.setState({renderImage: true});
    }

    // Choose image to render based off backend response
    chooseImage = () =>{
        switch(this.state.image){
            case 'a':
                this.setState({image: a, textToSpeak: 'a'});
                break;
            case 'b':
                this.setState({image: b, textToSpeak: 'b'});
                break;
            case 'c':
                this.setState({image: c, textToSpeak: 'c'});
                break;
            case 'd':
                this.setState({image: d, textToSpeak: 'd'});
                break;
            case 'e':
                this.setState({image: e, textToSpeak: 'e'});
                break;
            case 'f':
                this.setState({image: f, textToSpeak: 'f'});
                break;
            case 'g':
                this.setState({image: g, textToSpeak: 'g'});
                break;
            case 'h':
                this.setState({image: h, textToSpeak: 'h'});
                break;
            case 'i':
                this.setState({image: i, textToSpeak: 'i'});
                break;
            case 'j':
                this.setState({image: j, textToSpeak: 'j'});
                break;
            case 'k':
                this.setState({image: k, textToSpeak: 'k'});
                break;
            case 'l':
                this.setState({image: l, textToSpeak: 'l'});
                break;
            case 'm':
                this.setState({image: m, textToSpeak: 'm'});
                break;
            case 'n':
                this.setState({image: n, textToSpeak: 'n'});
                break;
            case 'o':
                this.setState({image: o, textToSpeak: 'o'});
                break;
            case 'p':
                this.setState({image: p, textToSpeak: 'p'});
                break;
            case 'q':
                this.setState({image: q, textToSpeak: 'q'});
                break;
            case 'r':
                this.setState({image: r, textToSpeak: 'r'});
                break;
            case 's':
                this.setState({image: s, textToSpeak: 's'});
                break;
            case 't':
                this.setState({image: t, textToSpeak: 't'});
                break;
            case 'u':
                this.setState({image: u, textToSpeak: 'u'});
                break;
            case 'v':
                this.setState({image: v, textToSpeak: 'v'});
                break;
            case 'w':
                this.setState({image: w, textToSpeak: 'w'});
                break;
            case 'x':
                this.setState({image: x, textToSpeak: 'x'});
                break;
            case 'y':
                this.setState({image: y, textToSpeak: 'y'});
                break;
            case 'z':
                this.setState({image: z, textToSpeak: 'z'});
                break;
            default:
                this.setState({image: ''})
                break;
        }
    }

    handleLetterPress = () =>{
        this.setState({renderLetterForm: true});
        if(this.state.renderWordList){
            this.setState({renderWordList: false});
        }
    }

    handleWordPress = () =>{
        this.setState({renderWordList: true});
        if(this.state.renderLetterForm){
            this.setState({renderLetterForm: false});
        }
    }

    render(){
        return(
            <div>
                <div>
                    <Jumbotron fluid>
                        <Container fluid>
                            <h1 className="display-3">Translator</h1>
                            <p className="lead">Want to learn some American Sign Language?</p>
                            <p className="lead">Well you're at the right place!</p>
                            <p className="lead">Choose between words and letters to see how they're signed.</p>
                            <p className="lead">Make sure to have your sound on so you can hear each word and letter!</p>
                        </Container>
                    </Jumbotron>
                </div>
                
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
                            <Label for="userInput">Enter a letter to see what it looks like in sign language</Label>
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
                    <div>
                        <h1>words</h1>
                    </div>
                :
                    null
                }

                

                
            </div>
        );
    }
}