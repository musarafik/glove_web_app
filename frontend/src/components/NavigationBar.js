import React from 'react'
import {Nav, Navbar} from 'react-bootstrap';
import styled from 'styled-components';

const Styles = styled.div`
    .navbar{
        background-color = #122;
    }
    .navbar-brand, .navbar-nav,  .nav-link{
        color: bbb;

        &:hover{
            color: teal;

        }
    }
    
`;   

const NavigationBar = () =>(
    <Styles>
        <Navbar bg="dark" variant="dark" expand="lg" >
            <Navbar.Brand href="/">I4: Sign Language Translator</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav"/>
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ml-auto">
                    <Nav.Item><Nav.Link href="/">Home</Nav.Link></Nav.Item>
                    <Nav.Item><Nav.Link href="/about">About</Nav.Link></Nav.Item>
                    <Nav.Item><Nav.Link href="/reports">Reports</Nav.Link></Nav.Item>
                    <Nav.Item><Nav.Link href="/translator">Translator</Nav.Link></Nav.Item>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    </Styles>
)

export default NavigationBar;

