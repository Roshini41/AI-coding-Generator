import { useState } from "react";

export function MCQChallenge({ challenge, showExplanation = false }) {
  const [selectedOption, setSelectedOption] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  const options =
    typeof challenge.options === "string"
      ? JSON.parse(challenge.options)
      : challenge.options;

  const handleSelect = (index) => {
    if (submitted) return;
    setSelectedOption(index);
  };

  const checkAnswer = () => {
    if (selectedOption === null) return;
    setSubmitted(true);
  };

  const getOptionClass = (index) => {
    if (!submitted) {
      return selectedOption === index ? "option selected" : "option";
    }

    if (index === challenge.correct_answer_id) {
      return "option correct";
    }

    if (
      index === selectedOption &&
      selectedOption !== challenge.correct_answer_id
    ) {
      return "option incorrect";
    }

    return "option";
  };

  return (
    <div className="challenge-display">
      <h3>{challenge.title}</h3>

      <p>
        <strong>Difficulty:</strong> {challenge.difficulty}
      </p>

      <div className="options">
        {options.map((option, index) => (
          <div
            key={index}
            className={getOptionClass(index)}
            onClick={() => handleSelect(index)}
          >
            {option}
          </div>
        ))}
      </div>

      {!submitted && (
        <button
          onClick={checkAnswer}
          disabled={selectedOption === null}
          className="generate-button"
        >
          Submit Answer
        </button>
      )}

      {submitted && (
        <>
          <h4>
            {selectedOption === challenge.correct_answer_id
              ? "✅ Correct!"
              : "❌ Wrong Answer"}
          </h4>

          <div className="explanation">
            <h4>Explanation</h4>
            <p>{challenge.explanation}</p>
          </div>
        </>
      )}
    </div>
  );
}