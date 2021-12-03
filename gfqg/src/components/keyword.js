import * as React from "react";
import Box from "@mui/material/Box";
import Input from "@mui/material/Input";
import { useState } from "react";
import { Button } from "@mui/material";
import { Select, MenuItem } from "@mui/material";
import { Grid } from "@mui/material";
const ariaLabel = { "aria-label": "description" };
export default function Inputs(props) {
  const { history } = props;
  const times = [];
  const days = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
  ];

  for (let i = 0; i <= 21; i++) {
    let x = i.toString();
    if (x.length < 2) x = "0" + x;
    x += ":00";
    times.push(x);
  }

  const [keyword, setKeyword] = useState("");
  const [approx, setApprox] = useState(10);
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState({});
  const [email, setEmail] = useState("abc@gmail.com");
  const [day, setDay] = useState("monday");
  const [time, setTime] = useState("00:00");
  const fetchQuestion = () => {
    setLoading(true);
    fetch(
      `http://localhost:5000/generate_from_keyword?query=${keyword}&max_questions=${approx}`
    )
      .then((res) => res.json())
      .then(async (data) => {
        let questions = {};
        data = await Promise.all(
          data.map((d, index) => {
            questions[index] = {
              question: d.pop(),
              answers: d.map((str) => str.toLowerCase()),
              selected: Array.from({ length: d.length }, (v, k) => "null"),
            };
            return d;
          })
        );
        setQuestions(questions);
        setLoading(false);
      })
      .catch((err) => {
        setLoading(false);
      });
  };

  const submitAnswers = async () => {
    let response = {
      question_data: [],
      revision_plan: {
        day: day,
        time: time,
      },
      email: email,
    };
    await Promise.all(
      Object.keys(questions).map((quest) => {
        let question = questions[quest];
        if (
          JSON.stringify(question.answers) !== JSON.stringify(question.selected)
        ) {
          response.question_data.push({
            question: question.question,
            correct_answer: question.answers.toString(),
            wrong_answer: question.selected.toString(),
          });
        }
        return question;
      })
    );
    console.log(response);
    fetch("http://localhost:5000/revisionEmail", {
      method: "POST",
      body: JSON.stringify(response),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    })
      .then((res) => {
        history.push("/thanks");
      })
      .catch((err) => alert("Some Error Occured Try Again" + err));
  };
  return (
    <>
      {Object.keys(questions).length < 1 && (
        <Box
          component="form"
          sx={{
            "& > :not(style)": { m: 1 },
            justifyContent: "center",
            alignContent: "center",
            width: "100%",
          }}
          noValidate
          autoComplete="off"
        >
          <Input
            defaultValue={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder={
              'Place keyword to Search example Delhi the capita"Hello world" l of India'
            }
            inputProps={ariaLabel}
            sx={{ width: "50%" }}
          />
          <Input
            onChange={(e) => setApprox(e.target.value)}
            type={"number"}
            placeholder={"Approx questions to generate"}
            inputProps={ariaLabel}
            sx={{ marginLeft: 10 }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={fetchQuestion}
            disabled={loading}
          >
            Submit
          </Button>
        </Box>
      )}
      {Object.keys(questions).length > 0 && (
        <Grid container alignItems="center" justifyContent="center">
          <h1>
            Answer these questions and submit the answers with your email and
            time scheduled for revision.
          </h1>
          <Grid
            item
            xs={8}
            sm={8}
            lg={8}
            md={8}
            sx={{ height: "90vh", width: "100%", overflowY: "scroll" }}
          >
            {Object.keys(questions).map((index) => {
              return (
                <>
                  <p>
                    Q.{1 + parseInt(index)}. {questions[index].question}
                  </p>
                  <br />
                  <Input
                    onChange={(e) => {
                      let qna = questions;
                      qna[index].selected = e.target.value
                        .toLowerCase()
                        .split(",");
                      setQuestions(qna);
                    }}
                    placeholder={"Enter Your answer."}
                    inputProps={ariaLabel}
                    sx={{ marginLeft: 10, width: "80%" }}
                  />
                  <br />
                </>
              );
            })}
          </Grid>
          <Grid
            container
            xs={12}
            sm={12}
            lg={12}
            md={12}
            item
            justifyContent="center"
            alignItems="center"
          >
            <Grid item xs={2} sm={2} lg={2} md={2}>
              <Input
                onChange={(e) => setEmail(e.target.value)}
                type={"email"}
                placeholder={"johndoe@example.com"}
                inputProps={ariaLabel}
                sx={{ marginLeft: 10 }}
              />
            </Grid>
            <Grid
              item
              xs={1}
              sm={1}
              lg={1}
              md={1}
              container
              justifyContent="flex-end"
            >
              <Select
                labelId="demo-simple-select-label2"
                id="demo-simple-select2"
                value={day}
                label={"day"}
                onChange={(e) => setDay(e.target.value)}
              >
                {days.map((d) => {
                  return (
                    <MenuItem value={d} selected={d === day}>
                      {" "}
                      {d}{" "}
                    </MenuItem>
                  );
                })}
              </Select>
            </Grid>
            <Grid
              item
              xs={1}
              sm={1}
              lg={1}
              md={1}
              container
              justifyContent="flex-start"
            >
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={time}
                label={"time"}
                onChange={(e) => setTime(e.target.value)}
              >
                {times.map((t) => {
                  return (
                    <MenuItem value={t} selected={t === time}>
                      {" "}
                      {t}{" "}
                    </MenuItem>
                  );
                })}
              </Select>
            </Grid>
            <Grid
              item
              xs={1}
              sm={1}
              lg={1}
              md={1}
              container
              justifyContent="flex-start"
            >
              <Button
                variant="contained"
                color="primary"
                onClick={submitAnswers}
              >
                Submit Answers
              </Button>
            </Grid>
          </Grid>
        </Grid>
      )}
    </>
  );
}
