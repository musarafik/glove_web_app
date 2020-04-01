import React from 'react';
import {Form, FormGroup, Label, Input, Button} from 'reactstrap';
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
        paddingTop: '10%'
    }
}

export default class Translator extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            renderImage: false,
            image: ''
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
                this.setState({image: a});
                break;
            case 'b':
                this.setState({image: b});
                break;
            case 'c':
                this.setState({image: c});
                break;
            case 'd':
                this.setState({image: d});
                break;
            case 'e':
                this.setState({image: e});
                break;
            case 'f':
                this.setState({image: f});
                break;
            case 'g':
                this.setState({image: g});
                break;
            case 'h':
                this.setState({image: h});
                break;
            case 'i':
                this.setState({image: i});
                break;
            case 'j':
                this.setState({image: j});
                break;
            case 'k':
                this.setState({image: k});
                break;
            case 'l':
                this.setState({image: l});
                break;
            case 'm':
                this.setState({image: m});
                break;
            case 'n':
                this.setState({image: n});
                break;
            case 'o':
                this.setState({image: o});
                break;
            case 'p':
                this.setState({image: p});
                break;
            case 'q':
                this.setState({image: q});
                break;
            case 'r':
                this.setState({image: r});
                break;
            case 's':
                this.setState({image: s});
                break;
            case 't':
                this.setState({image: t});
                break;
            case 'u':
                this.setState({image: u});
                break;
            case 'v':
                this.setState({image: v});
                break;
            case 'w':
                this.setState({image: w});
                break;
            case 'x':
                this.setState({image: x});
                break;
            case 'y':
                this.setState({image: y});
                break;
            case 'z':
                this.setState({image: z});
                break;
            default:
                this.setState({image: ''})
                break;
        }
    }

    render(){
        return(
            <div>
                <h2>Translator Page</h2>

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

                
            </div>
        );
    }
}