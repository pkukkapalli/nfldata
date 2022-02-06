import { Component } from "react";
import debounce from "lodash.debounce";
import { searchCoaches } from "./coachesApi";

/**
 * Component that renders the coaching tree for selected coaches.
 *
 * NOTE: we are using a class component here instead of the usual functional
 * component, because storing a debounced function in a functional component is
 * complicated, and hard to reason about.
 */
class CoachingTree extends Component {
  constructor(props) {
    super(props);
    this.state = { searchQuery: "", searchResults: [], errorMessage: "" };
    this.debouncedFetchSearchResults = debounce(
      () => this.fetchSearchResults(),
      /* wait= */ 500
    );
  }

  async fetchSearchResults() {
    const { success, coaches, errorMessage } = await searchCoaches({
      query: this.state.searchQuery,
    });
    if (success) {
      this.setState({ searchResults: coaches });
    } else {
      this.setState({ errorMessage });
    }
  }

  async onSearchQueryChanged(e) {
    this.setState({ searchQuery: e.target.value });
    await this.debouncedFetchSearchResults();
  }

  render() {
    return (
      <div>
        <h1>Coaching Tree</h1>
        <input
          value={this.state.searchQuery}
          onChange={this.onSearchQueryChanged.bind(this)}
        ></input>
        <ul>
          {this.state.searchResults.map(({ coach, name }) => (
            <li key={coach}>{name}</li>
          ))}
        </ul>
        <p>{this.state.errorMessage}</p>
      </div>
    );
  }
}

export default CoachingTree;
