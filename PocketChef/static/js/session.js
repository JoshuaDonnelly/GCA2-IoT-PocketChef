document.addEventListener('DOMContentLoaded', function() {
  const weightSlider = document.getElementById('weightSlider');
  const weightOutput = document.getElementById('currentWeight');
  const weightValueDiv = document.querySelector('.weightValue');
  const weightRangeDiv = document.querySelector('.weightRange');
  const tempSlider = document.getElementById('tempSlider');
  const tempOutput = document.getElementById('currentTemp');
  const tempValueDiv = document.querySelector('.tempValue');
  let isMetric = true;

  function updateWeightDisplay() {
    if (isMetric) {
      weightOutput.textContent = weightSlider.value;
      weightValueDiv.innerHTML = `<span id="currentWeight">${weightSlider.value}</span> Kg`;
    } else {
      const lbs = (weightSlider.value * 2.20462).toFixed(1);
      weightOutput.textContent = lbs;
      weightValueDiv.innerHTML = `<span id="currentWeight">${lbs}</span> lbs`;
    }
  }

  function updateTempDisplay() {
    if (isMetric) {
      tempOutput.textContent = tempSlider.value;
      tempValueDiv.innerHTML = `<span id="currentTemp">${tempSlider.value}</span> °C`;
    } else {
      const fahrenheit = (tempSlider.value * 9/5 + 32).toFixed(1);
      tempOutput.textContent = fahrenheit;
      tempValueDiv.innerHTML = `<span id="currentTemp">${fahrenheit}</span> °F`;
    }
  }

  weightSlider.oninput = updateWeightDisplay;
  tempSlider.oninput = updateTempDisplay;

  // Initialize both displays on page load
  updateWeightDisplay();
  updateTempDisplay();

  window.toggleMetricSystem = function() {
    isMetric = !isMetric;
    weightRangeDiv.textContent = isMetric ? 'Weight (Kg):' : 'Weight (lbs):';
    // Update both displays
    updateWeightDisplay();
    updateTempDisplay();
  };
});