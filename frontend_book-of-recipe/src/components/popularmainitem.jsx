import React, { Component } from 'react';
import { Row, Col, Container } from 'react-bootstrap';
import './popularmainitem.css';

export default class PopularMainItem extends Component {
  state = {}
  render() {
    return (
      <Row>
        <Col lg={1}></Col>
        <Col lg={6}>
          <Container className="img-container">
            <img src="./img/meet.jpg" alt="" />
          </Container>
        </Col>
        <Col lg={4}></Col>
        <Col lg={1}></Col>
      </Row>
    );
  }
}