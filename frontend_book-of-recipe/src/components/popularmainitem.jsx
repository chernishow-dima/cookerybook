import React, { Component } from 'react';
import { Row, Col, Container, Carousel } from 'react-bootstrap';
import './popularmainitem.css';

export default class PopularMainItem extends Component {
  state = {}
  render() {
    return (
      <Row>
        <Col lg={1}></Col>
        <Col lg={10}>
          <Carousel>
            <Carousel.Item>
              <div className="radial-gradient">
                <img
                  className="image d-block w-100"
                  src="./img/meet.jpg"
                  alt="First slide"
                />
              </div>
              <Carousel.Caption>
                <h3>Название 1 блюда</h3>
                <p>Рецепт</p>
              </Carousel.Caption>
            </Carousel.Item>
            <Carousel.Item>
              <div className="radial-gradient">
                <img
                  className="image d-block w-100"
                  src="./img/heart.png"
                  alt="First slide"
                />
              </div>

              <Carousel.Caption>
                <h3>Название 2 блюда</h3>
                <p>Рецепт</p>
              </Carousel.Caption>
            </Carousel.Item>
            <Carousel.Item>
              <div className="radial-gradient">
                <img
                  className="image d-block w-100"
                  src="./img/pancakes.jpg"
                  alt="First slide"
                />
              </div>
              <Carousel.Caption>
                <h3>Название 3 блюда</h3>
                <p>Рецепт</p>
              </Carousel.Caption>
            </Carousel.Item>
          </Carousel></Col>
        <Col lg={1}></Col>
      </Row>
    );
  }
}