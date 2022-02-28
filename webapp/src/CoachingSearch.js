import { Component } from "react";
import debounce from "lodash.debounce";
import { searchCoaches } from "./coachesApi";

/**
 * NOTE: we are using a class component here instead of the usual functional
 * component, because storing a debounced function in a functional component is
 * complicated, and hard to reason about.
 */
class CoachingSearch extends Component {
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
    const { searchQuery, searchResults } = this.state;
    return (
      <>
        <input
          value={searchQuery}
          onChange={this.onSearchQueryChanged.bind(this)}
        ></input>
        <ul>
          {searchResults.map(({ coach, name }) => (
            <li key={coach}>
              <button onClick={() => this.props.onSelect(coach)}>{name}</button>
            </li>
          ))}
        </ul>
      </>
    );
  }
}

export default CoachingSearch;
