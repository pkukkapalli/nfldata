const API = process.env.REACT_APP_API_SERVER_ADDRESS;

export async function searchCoaches({ query = "", limit = 10 }) {
  try {
    const response = await fetch(
      `${API}/api/coaches?query=${query}&limit=${limit}`
    );
    const { response: coaches } = await response.json();
    return { success: true, coaches };
  } catch (e) {
    return {
      success: false,
      errorMessage: "Failed to get coaches, please try again",
    };
  }
}
