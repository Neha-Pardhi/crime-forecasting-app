// Backend URL
const API_URL = "http://127.0.0.1:8000";

// Load Cities
async function loadCities() {
  const response = await fetch(`${API_URL}/cities`);
  const data = await response.json();
  const cityDropdown = document.getElementById("city");
  cityDropdown.innerHTML = data.cities.map(city => `<option value="${city}">${city}</option>`).join("");
}

// Load Crime Types
async function loadCrimeTypes() {
  const response = await fetch(`${API_URL}/crime_types`);
  const data = await response.json();
  const crimeDropdown = document.getElementById("crime");
  crimeDropdown.innerHTML = data.crime_types.map(crime => `<option value="${crime}">${crime}</option>`).join("");
}

// Predict
async function getPrediction() {
  const city = document.getElementById("city").value;
  const crime = document.getElementById("crime").value;
  const year = document.getElementById("year").value;

  if (!year) {
    alert("Please enter a year!");
    return;
  }

  const response = await fetch(`${API_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ city, crime_type: crime, year: parseInt(year) })
  });

  const result = await response.json();

  document.getElementById("result").innerHTML = `
    📍 City: ${result.city} <br>
    ⚖️ Crime Type: ${result.crime_type} <br>
    📅 Year: ${result.year} <br>
    🔮 Predicted Value: ${result.final_prediction}
  `;
}

// Load dropdowns on page load
window.onload = () => {
  loadCities();
  loadCrimeTypes();
};
