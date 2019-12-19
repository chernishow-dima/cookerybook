import React, { Component } from 'react';
import { Row, Button, Col, Container } from "react-bootstrap"
import { Link } from 'react-router-dom';
import "./navbar.css"
export default class Navbar extends Component {
    state = {}
    render() {
        return (
            <>
                <Row>
                    <Col lg="1">
                        <Link to="/" style={{ textDecoration: 'none' }}>
                            <Container bsPrefix='logoContainer'>
                                <p>ВКУС</p>
                            </Container>
                        </Link>
                    </Col>
                    <Col lg="8"></Col>
                    <Col lg="2">
                        <Link to="/recipe">
                            <Button variant="mybutton">
                                ПОПУЛЯРНОЕ
                            </Button>
                        </Link>
                    </Col>
                    <Col lg="1"></Col>
                </Row>
            </>
        );
    }
}

