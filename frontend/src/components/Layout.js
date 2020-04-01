import React from 'react';
import {Container} from 'react-bootstrap';

const Layout = (props) => (
    <Container style={{backgroundColor:'#f8f8ff'}}>
        {props.children}
    </Container>
) 

export default Layout;