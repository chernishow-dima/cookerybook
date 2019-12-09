import React, { Component } from 'react';
import { Form, Button, Row, Col, DropdownButton, Dropdown } from 'react-bootstrap';
import './searchform.css'
export default class SearchForm extends Component {
  state = {}
  render() {
    return (
      <Row>
        <Col lg={1}></Col>
        <Col lg={10}>
          <Form>
            <Form.Group controlId="formBasicEmail">
              <Form.Control type='input' placeholder="ПОИСК" />
            </Form.Group>
            <Form.Row>
              <Form.Group as={Col} controlId="formGridState">
                <Form.Control className="my_btn_dd" as="select">
                  <option>ЛЮБАЯ КУХНЯ</option>
                  <option>...</option>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col} controlId="formGridState">
                <Form.Control className="my_btn_dd" as="select">
                  <option>ЛЮБАЯ КАТЕГОРИЯ</option>
                  <option>...</option>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col} controlId="formGridState">
                <Form.Control className="my_btn_dd" as="select">
                  <option>ЛЮБОЕ МЕНЮ</option>
                  <option>...</option>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col} controlId="formGridState">
                <Form.Control className="my_btn_dd" as="select">
                  <option>ИНГРЕДИЕНТЫ</option>
                  <option>...</option>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
                <Button type="submit" className="my_btn">ПОДОБРАТЬ РЕЦЕПТЫ</Button>
              </Form.Group>
            </Form.Row>
          </Form >
        </Col>
        <Col lg={1}></Col>
      </Row >
    );
  }
}

