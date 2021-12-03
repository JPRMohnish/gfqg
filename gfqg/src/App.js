import "./App.css";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import keyword from "./components/keyword";
import thankYou from "./components/thankYou";
function App() {
  return (
    <>
      <Router>
        <Switch>
          <Route path="/questions" component={keyword} />
          <Route path="/thanks" component={thankYou} />
        </Switch>
      </Router>
    </>
  );
}

export default App;
