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

    // Send response to backend in json with POST request whenever page loads
    handleOnSubmit(event){
        event.preventDefault();
        console.log(event);
        // fetch('backend url', { // TODO: fill in route with backend info
        //     method: 'POST',
        //     mode: 'cors',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify(data)
        // })
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