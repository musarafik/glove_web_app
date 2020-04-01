import React from 'react';
import {Form, FormGroup, Label, Input, Button} from 'reactstrap';

const styles = {
    inputContainer:{
        display: 'flex',
        flexDirection: 'row',
    }
}

export default class Translator extends React.Component{
    constructor(props){
        super(props);
        this.state = {}
    }

    // Send response to backend in json form with POST request whenever form is submitted
    handleOnSubmit(event){
        event.preventDefault();
        fetch('/translator', { 
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(event.target.userInput.value)
        })
        .then(response => response.json())
        .then(data => console.log(data))
    }

    render(){
        return(
            <div>
                <h2>Translator Page</h2>

                <Form onSubmit={this.handleOnSubmit}>
                    <FormGroup style={{paddingTop: '5%'}}>
                        <Label for="userInput">Enter a letter to see what it looks like in sign language</Label>
                        <div style={styles.inputContainer}>
                            <Input type="textArea" name="input" id="userInput" />
                            <Button style={{marginLeft: '1%'}}>Submit</Button>
                        </div>
                    </FormGroup>
                </Form>

            </div>
        );
    }
}