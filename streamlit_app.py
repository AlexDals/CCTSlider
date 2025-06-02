<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CCT Color Temperature Tool</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            min-height: 100vh;
            color: #334155;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.08);
            border: 1px solid rgba(255,255,255,0.2);
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header p {
            color: #64748b;
            font-size: 1.1rem;
        }

        .card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 24px rgba(0,0,0,0.06);
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
        }

        .card h2 {
            color: #1e293b;
            font-size: 1.4rem;
            margin-bottom: 1.5rem;
            font-weight: 600;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #374151;
        }

        select, input[type="number"] {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: white;
        }

        select:focus, input[type="number"]:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .slider-container {
            position: relative;
            margin: 1.5rem 0;
        }

        .slider {
            width: 100%;
            height: 8px;
            border-radius: 4px;
            background: linear-gradient(to right, #ff6b35, #f7931e, #ffff00, #87ceeb, #4169e1);
            outline: none;
            -webkit-appearance: none;
            appearance: none;
        }

        .slider::-webkit-slider-thumb {
            appearance: none;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: white;
            cursor: pointer;
            border: 3px solid #3b82f6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }

        .slider::-moz-range-thumb {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: white;
            cursor: pointer;
            border: 3px solid #3b82f6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }

        .controls-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
            align-items: end;
        }

        .preset-buttons {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 1.5rem;
        }

        .preset-btn {
            padding: 0.5rem 1rem;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            background: white;
            color: #374151;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }

        .preset-btn:hover {
            border-color: #3b82f6;
            background: #f0f9ff;
            color: #1d4ed8;
            transform: translateY(-1px);
        }

        .color-preview {
            display: grid;
            grid-template-columns: 1fr 200px;
            gap: 2rem;
            align-items: center;
        }

        .color-info {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .color-info-item {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
        }

        .color-info-label {
            font-weight: 500;
            color: #374151;
        }

        .color-info-value {
            font-family: 'Courier New', monospace;
            color: #6b7280;
            background: #f3f4f6;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }

        .color-swatch {
            width: 180px;
            height: 120px;
            border-radius: 15px;
            border: 3px solid #e5e7eb;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .reference-colors {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .reference-item {
            text-align: center;
        }

        .reference-swatch {
            width: 100%;
            height: 80px;
            border-radius: 10px;
            border: 2px solid #e5e7eb;
            margin-bottom: 0.5rem;
            transition: all 0.3s ease;
        }

        .reference-swatch:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }

        .reference-label {
            font-size: 0.9rem;
            font-weight: 600;
            color: #374151;
        }

        .reference-desc {
            font-size: 0.8rem;
            color: #6b7280;
        }

        .current-temp {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1rem;
        }

        .temp-description {
            font-size: 1.1rem;
            color: #3b82f6;
            font-weight: 500;
            margin-bottom: 1rem;
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .controls-grid {
                grid-template-columns: 1fr;
            }
            
            .color-preview {
                grid-template-columns: 1fr;
                text-align: center;
            }
            
            .color-swatch {
                margin: 0 auto;
            }
            
            .reference-colors {
                grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💡 CCT Color Temperature Tool</h1>
            <p>Professional color temperature visualization with accurate warm and cool white rendering</p>
        </div>

        <div class="card">
            <h2>🎛️ Range Selection</h2>
            <div class="form-group">
                <label for="cctRange">CCT Range:</label>
                <select id="cctRange" onchange="updateRange()">
                    <option value="2200-4000">2200K - 4000K (Warm Whites)</option>
                    <option value="2700-6500">2700K - 6500K (Full Range)</option>
                </select>
            </div>
        </div>

        <div class="card">
            <h2>🔄 Temperature Control</h2>
            <div class="controls-grid">
                <div>
                    <label for="slider">Slider Value (0-1000):</label>
                    <div class="slider-container">
                        <input type="range" id="slider" class="slider" min="0" max="1000" value="0" oninput="updateFromSlider()">
                    </div>
                </div>
                <div class="form-group">
                    <label for="cctInput">CCT Value (K):</label>
                    <input type="number" id="cctInput" min="2200" max="6500" value="2200" oninput="updateFromCCT()">
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🎯 Quick Presets</h2>
            <div class="preset-buttons" id="presetButtons">
                <!-- Preset buttons will be generated by JavaScript -->
            </div>
        </div>

        <div class="card">
            <h2>🎨 Color Preview</h2>
            <div class="current-temp" id="currentTemp">2200K</div>
            <div class="temp-description" id="tempDescription">Very Warm White</div>
            
            <div class="color-preview">
                <div class="color-info">
                    <div class="color-info-item">
                        <span class="color-info-label">RGB Values:</span>
                        <span class="color-info-value" id="rgbValue">(255, 147, 41)</span>
                    </div>
                    <div class="color-info-item">
                        <span class="color-info-label">Hex Code:</span>
                        <span class="color-info-value" id="hexValue">#ff9329</span>
                    </div>
                    <div class="color-info-item">
                        <span class="color-info-label">Temperature:</span>
                        <span class="color-info-value" id="tempValue">2200K</span>
                    </div>
                </div>
                <div class="color-swatch" id="colorSwatch">
                    2200K
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🌡️ Reference Temperatures</h2>
            <div class="reference-colors" id="referenceColors">
                <!-- Reference colors will be generated by JavaScript -->
            </div>
        </div>
    </div>

    <script>
        let currentRange = '2200-4000';
        let minCCT = 2200;
        let cctPerUnit = 1.8;
        let presetValues = [2200, 2700, 3000, 3500, 4000];

        function sliderToCCT(sliderValue) {
            return minCCT + sliderValue * cctPerUnit;
        }

        function cctToSlider(cctValue) {
            return (cctValue - minCCT) / cctPerUnit;
        }

        function updateRange() {
            const rangeSelect = document.getElementById('cctRange');
            currentRange = rangeSelect.value;
            
            if (currentRange === '2200-4000') {
                minCCT = 2200;
                cctPerUnit = 1.8;
                presetValues = [2200, 2700, 3000, 3500, 4000];
            } else {
                minCCT = 2700;
                cctPerUnit = 3.8;
                presetValues = [2700, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500];
            }
            
            updatePresetButtons();
            updateFromSlider();
            updateCCTInput();
        }

        function updatePresetButtons() {
            const container = document.getElementById('presetButtons');
            container.innerHTML = '';
            
            presetValues.forEach(value => {
                const button = document.createElement('button');
                button.className = 'preset-btn';
                button.textContent = value + 'K';
                button.onclick = () => setPreset(value);
                container.appendChild(button);
            });
        }

        function setPreset(cctValue) {
            const sliderValue = cctToSlider(cctValue);
            document.getElementById('slider').value = sliderValue;
            updateFromSlider();
        }

        function updateFromSlider() {
            const slider = document.getElementById('slider');
            const cctValue = sliderToCCT(parseFloat(slider.value));
            document.getElementById('cctInput').value = Math.round(cctValue);
            updateDisplay(cctValue);
        }

        function updateFromCCT() {
            const cctInput = document.getElementById('cctInput');
            const cctValue = parseFloat(cctInput.value);
            const sliderValue = cctToSlider(cctValue);
            
            if (sliderValue >= 0 && sliderValue <= 1000) {
                document.getElementById('slider').value = sliderValue;
                updateDisplay(cctValue);
            }
        }

        function updateCCTInput() {
            const cctInput = document.getElementById('cctInput');
            cctInput.min = minCCT;
            cctInput.max = minCCT + 1000 * cctPerUnit;
        }

        function cctToRGB(cct) {
            cct = Math.max(1000, Math.min(40000, cct));
            const temp = cct / 100.0;
            
            let red, green, blue;
            
            // Calculate Red
            if (temp <= 66) {
                red = 255;
            } else {
                red = temp - 60;
                red = 329.698727446 * Math.pow(red, -0.1332047592);
                red = Math.max(0, Math.min(255, red));
            }
            
            // Calculate Green
            if (temp <= 66) {
                green = temp;
                green = 99.4708025861 * Math.log(green) - 161.1195681661;
                green = Math.max(0, Math.min(255, green));
            } else {
                green = temp - 60;
                green = 288.1221695283 * Math.pow(green, -0.0755148492);
                green = Math.max(0, Math.min(255, green));
            }
            
            // Calculate Blue
            if (temp >= 66) {
                blue = 255;
            } else if (temp <= 19) {
                blue = 0;
            } else {
                blue = temp - 10;
                blue = 138.5177312231 * Math.log(blue) - 305.0447927307;
                blue = Math.max(0, Math.min(255, blue));
            }
            
            // Apply gamma correction
            function gammaCorrect(value) {
                const normalized = value / 255.0;
                const corrected = Math.pow(normalized, 1.0 / 2.2);
                return Math.floor(corrected * 255);
            }
            
            return [gammaCorrect(red), gammaCorrect(green), gammaCorrect(blue)];
        }

        function getColorDescription(cct) {
            if (cct < 2000) return "Candlelight";
            if (cct < 2700) return "Very Warm White";
            if (cct < 3000) return "Warm White";
            if (cct < 3500) return "Soft White";
            if (cct < 4000) return "Neutral White";
            if (cct < 5000) return "Cool White";
            if (cct < 6000) return "Daylight";
            if (cct < 7000) return "Cool Daylight";
            return "Blue Sky";
        }

        function updateDisplay(cctValue) {
            const [r, g, b] = cctToRGB(cctValue);
            const hex = `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
            const description = getColorDescription(cctValue);
            
            document.getElementById('currentTemp').textContent = Math.round(cctValue) + 'K';
            document.getElementById('tempDescription').textContent = description;
            document.getElementById('rgbValue').textContent = `(${r}, ${g}, ${b})`;
            document.getElementById('hexValue').textContent = hex;
            document.getElementById('tempValue').textContent = Math.round(cctValue) + 'K';
            
            const swatch = document.getElementById('colorSwatch');
            swatch.style.backgroundColor = hex;
            swatch.style.color = (r + g + b) > 400 ? 'black' : 'white';
            swatch.textContent = Math.round(cctValue) + 'K';
        }

        function initializeReferenceColors() {
            const referenceTemps = [2700, 3000, 4000, 5000, 6500];
            const container = document.getElementById('referenceColors');
            
            referenceTemps.forEach(temp => {
                const [r, g, b] = cctToRGB(temp);
                const hex = `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
                const description = getColorDescription(temp);
                
                const item = document.createElement('div');
                item.className = 'reference-item';
                item.innerHTML = `
                    <div class="reference-swatch" style="background-color: ${hex}"></div>
                    <div class="reference-label">${temp}K</div>
                    <div class="reference-desc">${description}</div>
                `;
                container.appendChild(item);
            });
        }

        // Initialize the application
        updatePresetButtons();
        updateFromSlider();
        updateCCTInput();
        initializeReferenceColors();
    </script>
</body>
</html>
