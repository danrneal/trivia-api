import React, { Component } from 'react';
import '../stylesheets/Question.css';

const starArray = [1, 2, 3, 4, 5];

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  render() {
    const { question, answer, category, difficulty, rating } = this.props;
    return (
      <div className="Question-holder">
        <div className="Question">{question}</div>
        <div className="Question-status">
          <img
            className="category"
            src={`${category.toLowerCase()}.svg`}
            alt={`${category}`}
          />
          <div className="rating">
            {starArray.map((num) => (
              <img
                key={num}
                src={`star${rating >= num ? '' : '-black'}.png`}
                alt={`star ${rating >= num ? 'active' : ''}`}
                className="star"
                onClick={() => {
                  this.props.questionAction('PATCH', num);
                }}
              />
            ))}
          </div>
          <div className="difficulty">Difficulty: {difficulty}</div>
          <img
            src="delete.png"
            alt="delete"
            className="delete"
            onClick={() => this.props.questionAction('DELETE')}
          />
        </div>
        <div
          className="show-answer button"
          onClick={() => this.flipVisibility()}
        >
          {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
        </div>
        <div className="answer-holder">
          <span
            style={{
              // stylelint-disable-next-line value-keyword-case
              visibility: this.state.visibleAnswer ? 'visible' : 'hidden',
            }}
          >
            Answer: {answer}
          </span>
        </div>
      </div>
    );
  }
}

export default Question;
