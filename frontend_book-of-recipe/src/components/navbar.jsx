import React, { Component } from 'react';
import { Row, Button, Col, Container } from "react-bootstrap"
import "./navbar.css"
export default class Navbar extends Component {
    state = {}
    render() {
        return (
            <>
                <Row>
                    <Col lg="1">
                        <Container bsPrefix='logoContainer'>
                            <p>ВКУС</p>
                        </Container>
                    </Col>
                    <Col lg="8"></Col>
                    <Col lg="2"><Button variant="mybutton">ПОПУЛЯРНОЕ</Button></Col>
                    <Col lg="1"></Col>
                </Row>
            </>
        );
    }
}

