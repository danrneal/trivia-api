import $ from 'jquery';
import React, { Component } from 'react';
import '../stylesheets/QuizView.css';

const questionsPerPlay = 5;

class QuizView extends Component {
  constructor(props) {
    super();
    this.state = {
      quizCategoryId: null,
      quizUserId: 1,
      previousQuestionIds: [],
      showAnswer: false,
      categories: {},
      users: {},
      numCorrect: 0,
      score: null,
      currentQuestion: {},
      guess: '',
      forceEnd: false,
    };
  }

  componentDidMount() {
    $.ajax({
      url: `/categories`,
      type: 'GET',
      success: (result) => {
        this.setState({ categories: result.categories });
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again');
        return;
      },
    });
    $.ajax({
      url: '/users',
      type: 'GET',
      success: (result) => {
        this.setState({ users: result.users });
        return;
      },
      error: (error) => {
        alert('Unable to load users. Please try your request again');
        return;
      },
    });
  }

  selectCategory = ({ id = 0 }) => {
    this.setState({ quizCategoryId: id }, this.getNextQuestion);
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  getNextQuestion = () => {
    const previousQuestionIds = [...this.state.previousQuestionIds];
    if (this.state.currentQuestion.id) {
      previousQuestionIds.push(this.state.currentQuestion.id);
    }

    $.ajax({
      url: '/quizzes',
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_question_ids: previousQuestionIds,
        quiz_category_id: this.state.quizCategoryId,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          showAnswer: false,
          previousQuestionIds: previousQuestionIds,
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false : true,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again');
        return;
      },
    });
  };

  submitGuess = (event) => {
    event.preventDefault();
    let evaluate = this.evaluateAnswer();
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true,
    });
  };

  updateScore = () => {
    $.ajax({
      url: `/users/${this.state.quizUserId}`,
      type: 'PATCH',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ score: this.state.numCorrect }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({ score: result.new_score });
        return;
      },
      error: (error) => {
        alert('Unable to update score. Please try your request again');
        return;
      },
    });
  };

  restartGame = () => {
    this.setState({
      quizCategoryId: null,
      previousQuestionIds: [],
      showAnswer: false,
      numCorrect: 0,
      score: null,
      currentQuestion: {},
      guess: '',
      forceEnd: false,
    });
  };

  renderPrePlay() {
    return (
      <div className="quiz-play-holder">
        <div className="choose-header">Choose User</div>
        <form className="form-view" id="choose_user-form">
          <label>
            User
            <select name="quizUserId" onChange={this.handleChange}>
              {Object.keys(this.state.users).map((id) => {
                return (
                  <option key={id} value={id}>
                    {id} - {this.state.users[id]}
                  </option>
                );
              })}
            </select>
          </label>
        </form>
        <hr></hr>
        <div className="choose-header">Choose Category</div>
        <div className="category-holder">
          <div className="play-category" onClick={this.selectCategory}>
            ALL
          </div>
          {Object.keys(this.state.categories).map((id) => {
            return (
              <div
                key={id}
                value={id}
                className="play-category"
                onClick={() => this.selectCategory({ id })}
              >
                {this.state.categories[id]}
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  renderFinalScore() {
    if (this.state.score === null) {
      this.updateScore();
    }
    return (
      <div className="quiz-play-holder">
        <div className="final-header">
          {' '}
          Your Final Score is {this.state.numCorrect}
        </div>
        <div className="lifetime-header">
          {' '}
          Your Lifetime Score is {this.state.score}
        </div>
        <div className="play-again button" onClick={this.restartGame}>
          {' '}
          Play Again?{' '}
        </div>
      </div>
    );
  }

  evaluateAnswer = () => {
    const formatGuess = this.state.guess
      .replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, '')
      .toLowerCase();
    const answerArray = this.state.currentQuestion.answer
      .toLowerCase()
      .split(' ');
    return answerArray.includes(formatGuess);
  };

  renderCorrectAnswer() {
    let evaluate = this.evaluateAnswer();
    return (
      <div className="quiz-play-holder">
        <div className="quiz-question">
          {this.state.currentQuestion.question}
        </div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>
          {evaluate ? 'You were correct!' : 'You were incorrect'}
        </div>
        <div className="quiz-answer">{this.state.currentQuestion.answer}</div>
        <div className="next-question button" onClick={this.getNextQuestion}>
          {' '}
          Next Question{' '}
        </div>
      </div>
    );
  }

  renderPlay() {
    return this.state.previousQuestionIds.length === questionsPerPlay ||
      this.state.forceEnd ? (
      this.renderFinalScore()
    ) : this.state.showAnswer ? (
      this.renderCorrectAnswer()
    ) : (
      <div className="quiz-play-holder">
        <div className="quiz-question">
          {this.state.currentQuestion.question}
        </div>
        <form onSubmit={this.submitGuess}>
          <input type="text" name="guess" onChange={this.handleChange} />
          <input
            className="submit-guess button"
            type="submit"
            value="Submit Answer"
          />
        </form>
      </div>
    );
  }

  render() {
    return this.state.quizCategoryId != null
      ? this.renderPlay()
      : this.renderPrePlay();
  }
}

export default QuizView;
