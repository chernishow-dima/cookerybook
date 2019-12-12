import React, { Component } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import Select from 'react-select';

import './searchform.css'

const options = [
  { value: 'chocolate', label: 'Chocolate' },
  { value: 'strawberry', label: 'Strawberry' },
  { value: 'vanilla', label: 'Vanilla' },
];

const customStyles = {

  option: (provided, state) => ({
    ...provided,
    color: "#000",
    textAlign: "center",
    backgroundColor: state.isSelected ? "#30FFB7" : "#fff",
    padding: 2,
    "&:hover": {
      backgroundColor: "#30FFB7",
    }
  }),

  control: (base, state) => ({
    ...base,
    width: "100%",
    height: "50px",
    fontFamily: 'Cinzel',
    fontSize: "12px",
    lineHeight: "14px",
    borderColor: state.isFocused ? "#30FFB7" : "#fff",
    boxShadow: null,

    "&:hover": {
      borderColor: "#30FFB7"
    },
    "&:focus": {
      borderColor: "#30FFB7"
    }
  })
};

export default class SearchForm extends Component {

  state = {
    selectedOption_kitchen: null,
    selectedOption_category: null,
    selectedOption_menu: null,
    selectedOption_ingredients: null,
  };

  handleChange_kitchen = selectedOption_kitchen => {
    this.setState(
      { selectedOption_kitchen },
      () => console.log(`Option selected:`, this.state.selectedOption_kitchen)
    );
  };
  handleChange_category = selectedOption_category => {
    this.setState(
      { selectedOption_category },
      () => console.log(`Option selected:`, this.state.selectedOption_category)
    );
  };
  handleChange_menu = selectedOption_menu => {
    this.setState(
      { selectedOption_menu },
      () => console.log(`Option selected:`, this.state.selectedOption_menu)
    );
  };
  handleChange_ingredients = selectedOption_ingredients => {
    this.setState(
      { selectedOption_ingredients },
      () => console.log(`Option selected:`, this.state.selectedOption_ingredients)
    );
  };

  render() {
    const { selectedOption_category, selectedOption_ingredients, selectedOption_kitchen, selectedOption_menu } = this.state;
    return (
      <>
        <Row>
          <Col lg={1}></Col>
          <Col lg={10}>
            <div className="input-field-container">
              <img src="./img/search.png" alt="" />
              <Form.Control type='input' placeholder="ПОИСК" className="input-field" />
            </div>
          </Col>
          <Col lg={1}></Col>
        </Row>
        <Row className="form-line">
          <Col lg={1}></Col>
          <Col lg={2}>
            <Select
              value={selectedOption_kitchen}
              styles={customStyles}
              indicatorSeparator={false}
              placeholder={"КУХНЯ"}
              options={options}
              onChange={this.handleChange_kitchen}
            />

          </Col>
          <Col lg={2}>
            <Select
              value={selectedOption_category}
              styles={customStyles}
              indicatorSeparator={false}
              placeholder={"КАТЕГОРИЯ"}
              options={options}
              onChange={this.handleChange_category}
            />
          </Col>
          <Col lg={2}>
            <Select
              value={selectedOption_menu}
              styles={customStyles}
              indicatorSeparator={false}
              placeholder={"МЕНЮ"}
              options={options}
              onChange={this.handleChange_menu}
            />
          </Col>
          <Col lg={2}>
            <Select
              value={selectedOption_ingredients}
              styles={customStyles}
              indicatorSeparator={false}
              placeholder={"ИНГРЕДИЕНТЫ"}
              options={options}
              onChange={this.handleChange_ingredients}
            />
          </Col>
          <Col lg={2}><Button bsPrefix="my_btn">ПОДОБРАТЬ РЕЦЕПТЫ</Button></Col>
          <Col lg={1}></Col>
        </Row>
      </>
    );
  }
}

