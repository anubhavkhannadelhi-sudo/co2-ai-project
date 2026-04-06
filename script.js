let usageCount = 0;
let chart;
let actualData = [];
let predictedData = [];
let autoMode = false;

// ✅ YOUR LIVE BACKEND URL
const BACKEND_URL = "https://co2-ai-project-3v0r.onrender.com/predict";

// ======================
// CO2 ESTIMATION (fallback)
// ======================
function estimateCO2(pm, temp, people){
    return 400 + (pm * 2) + (temp * 3) + (people * 20);
}

// ======================
// STATUS LOGIC
// ======================
function getCondition(co2){
    if(co2 < 600) return "Safe";
    if(co2 < 1000) return "Warning";
    return "Critical";
}

function getVent(co2){
    return co2 > 800 ? "ON" : "OFF";
}

// ======================
// COLUMN DETECTION
// ======================
function detectColumns(headers){
    let map = { pm:-1, temp:-1, co2:-1 };

    headers.forEach((h,i)=>{
        let name = h.toLowerCase();

        if(name.includes("pm")) map.pm = i;
        if(name.includes("temp")) map.temp = i;
        if(name.includes("co2")) map.co2 = i;
    });

    return map;
}

// ======================
// BACKEND CALL
// ======================
async function predictSingle(pm, temp, people){
    try{
        const res = await fetch(BACKEND_URL,{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify({
                pm25: pm,
                temp: temp,
                people: people
            })
        });

        return await res.json();

    }catch(err){
        alert("Backend not reachable!");
        console.error(err);
        return null;
    }
}

// ======================
// LIVE INPUT
// ======================
async function livePredict(){

    let pm = parseFloat(document.getElementById("live_pm").value);
    let temp = parseFloat(document.getElementById("live_temp").value);
    let people = parseInt(document.getElementById("people").value) || 1;

    if(isNaN(pm) || isNaN(temp)){
        alert("Enter valid inputs!");
        return;
    }

    usageCount++;
    document.getElementById("usage").innerText =
        "Usage Count: " + usageCount;

    let result = await predictSingle(pm,temp,people);
    if(!result) return;

    let pred = result.co2;
    let actual = estimateCO2(pm,temp,people);

    updateSystem(actual, pred);
}

// ======================
// DATASET PROCESSING
// ======================
async function processFile(){

    const file = document.getElementById("fileInput").files[0];
    if(!file) return alert("Upload dataset!");

    let people = parseInt(document.getElementById("people").value) || 1;

    const reader = new FileReader();

    reader.onload = async function(e){

        let lines = e.target.result.split("\n");
        let headers = lines[0].split(",");

        let map = detectColumns(headers);

        if(map.pm === -1 && map.co2 === -1){
            alert("Dataset must contain PM or CO2 column");
            return;
        }

        actualData = [];
        predictedData = [];

        for(let i=1;i<lines.length;i++){

            let cols = lines[i].split(",");

            let pm = map.pm !== -1 ? parseFloat(cols[map.pm]) : 50;
            let temp = map.temp !== -1 ? parseFloat(cols[map.temp]) : 25;
            let co2_actual = map.co2 !== -1 ? parseFloat(cols[map.co2]) : null;

            if(map.co2 !== -1){
                actualData.push(co2_actual);

                let result = await predictSingle(pm,temp,people);
                if(!result) return;

                predictedData.push(result.co2);

            }else{
                if(isNaN(pm) || isNaN(temp)) continue;

                let result = await predictSingle(pm,temp,people);
                if(!result) return;

                actualData.push(estimateCO2(pm,temp,people));
                predictedData.push(result.co2);
            }
        }

        drawGraph();
        updateUI(predictedData.at(-1));
        updateVisuals(predictedData.at(-1));
    };

    reader.readAsText(file);
}

// ======================
// SYSTEM UPDATE
// ======================
function updateSystem(actual, predicted){
    actualData.push(actual);
    predictedData.push(predicted);

    drawGraph();
    updateUI(predicted);
    updateVisuals(predicted);
}

// ======================
// UI UPDATE
// ======================
function updateUI(co2){

    document.getElementById("co2").innerText = co2.toFixed(2);

    document.getElementById("condition").innerText = getCondition(co2);
    document.getElementById("vent").innerText = getVent(co2);

    document.getElementById("trend").innerText =
        predictedData.length > 1 ?
        (predictedData.at(-1) > predictedData.at(-2) ? "↑" : "↓")
        : "--";

    document.getElementById("co2").style.color =
        co2 > 1000 ? "red" :
        co2 > 800 ? "yellow" : "#64ffda";
}

// ======================
// GRAPH
// ======================
function drawGraph(){

    const ctx = document.getElementById("co2Chart");

    if(chart) chart.destroy();

    chart = new Chart(ctx,{
        type:"line",
        data:{
            labels: actualData.map((_,i)=>i),
            datasets:[
                {
                    label:"Actual CO2",
                    data: actualData,
                    borderColor:"#64ffda"
                },
                {
                    label:"Predicted CO2",
                    data: predictedData,
                    borderColor:"#00ff99"
                }
            ]
        }
    });
}

// ======================
// VISUAL SIMULATION
// ======================
function updateVisuals(co2){

    let fill = document.getElementById("co2Fill");
    fill.style.height = Math.min(co2/2000*100,100)+"%";

    let fan = document.getElementById("fan");
    let status = document.getElementById("fanStatus");

    if(co2 > 800){
        fan.classList.add("spin");
        status.innerText = "Ventilation ON";
    }else{
        fan.classList.remove("spin");
        status.innerText = "Ventilation OFF";
    }
}

// ======================
// AUTO MODE
// ======================
function startAutoMode(){

    if(autoMode) return;
    autoMode = true;

    setInterval(()=>{
        let pm = Math.random()*150;
        let temp = 20 + Math.random()*10;
        let people = Math.floor(Math.random()*10)+1;

        document.getElementById("live_pm").value = pm.toFixed(1);
        document.getElementById("live_temp").value = temp.toFixed(1);
        document.getElementById("people").value = people;

        livePredict();
    },3000);
}