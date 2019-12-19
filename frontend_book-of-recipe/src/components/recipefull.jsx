import React, { Component } from 'react';
import { Row, Col, Container } from 'react-bootstrap';
import './recipefull.css'

export default class RecipeFull extends Component {
  constructor(props) {
    super(props);
    this.state = {}
  }
  render() {
    return (
      <>
        <Container>
          <Row>
            <Col lg={1}></Col>
            <Col lg={10}>
              <Container className="recipe-title-container">
                Название рецепта
              </Container>
              <Container className="recipe-data">
                <Row>
                  <Col>Описание Lorem ipsum dolor sit amet consectetur, adipisicing elit. Illo, et aperiam. Numquam quas ipsa cumque ducimus corporis provident odio nesciunt culpa et? Atque minus ex blanditiis, excepturi sapiente facilis dolorem.</Col>
                </Row>
              </Container>
            </Col>
            <Col lg={1}></Col>
          </Row>
          <Row>
            <Col lg={1}></Col>
            <Col lg={5}>
              <img
                className="recipe-image"
                src="./img/meet.jpg"
                alt="First slide"
              />
            </Col>
            <Col lg={5}>
              <Container className="recipe-data">
                <Row>
                  <Col>Калорийность</Col>
                  <Col>777ккал</Col>
                </Row>
                <hr />
                <Row>
                  <Col>Кухня</Col>
                  <Col>Название кухни</Col>
                </Row>
                <hr />
                <Row>
                  <Col>Используемые ингредиенты</Col>
                  <Col>Ингредиенты</Col>
                </Row>
              </Container>
            </Col>
            <Col lg={1}></Col>
          </Row>
        </Container>
      </>
    );
  }
}
