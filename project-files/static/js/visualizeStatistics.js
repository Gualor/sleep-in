//HR
var hr_table = document.getElementById('hr');
var hr = [];
var hr_label = [];
var hr_maxthres = [];
var hr_minthres = [];

//BMI
var bmi_table = document.getElementById('bmi');
var bmi = [];
var bmi_label = [];
var bmi_maxthres = [];
var bmi_minthres = [];

//SBP
var sbp_table = document.getElementById('sbp');
var sbp = [];
var sbp_label = [];
var sbp_maxthres = [];
var sbp_minthres = [];

//DBP
var dbp_table = document.getElementById('dbp');
var dbp = [];
var dbp_label = [];
var dbp_maxthres = [];
var dbp_minthres = [];

//CAL
var cal_table = document.getElementById('cal');
var cal = [];
var cal_label = [];
var cal_maxthres = [];
var cal_minthres = [];

//ACT
var act_table = document.getElementById('act');
var act = [];
var act_label = [];
var act_minthres = [];

//PSQ
var psq_table = document.getElementById('psq');
var psq = [];
var psq_label = [];
var psq_minthres = [];

//QUA
var qua_table = document.getElementById('qua');
var qua = [];
var qua_label = [];
var qua_minthres = [];

//EFF
var eff_table = document.getElementById('eff');
var eff = [];
var eff_label = [];
var eff_minthres = [];

//PSL 
var psl_table = document.getElementById('psl');
var psl = [];
var psl_label = [];
var psl_minthres = [];
var psl_maxthres = [];

//THRESHOLDS
var thresholds = document.getElementById('thresh');

if (thresholds == null) {
    var id = "Patient ID"
} else id = " ";



//------------------Create arrays---------------------------
//HR
for (var i = 0; i < hr_table.rows.length; i++) {
    var day = hr_table.rows[i].cells[0].innerHTML
    var value = hr_table.rows[i].cells[1].innerHTML
    if (thresholds == null) {
        var min_thres = 50
        var max_thres = 90
    } else {
        max_thres = thresholds.rows[3].cells[1].innerHTML
        min_thres = thresholds.rows[2].cells[1].innerHTML
    }
    var hr_max = parseInt(max_thres, 10) + 20
    var hr_min = parseInt(min_thres, 10) - 20
    console.log(hr_max)
    hr_label.push(day)
    hr.push(value)
    hr_maxthres.push(max_thres)
    hr_minthres.push(min_thres)
};

//BMI
for (var i = 0; i < bmi_table.rows.length; i++) {
    var day = bmi_table.rows[i].cells[0].innerHTML
    var value = bmi_table.rows[i].cells[1].innerHTML
    if (thresholds == null) {
        var min_thres = 12
        var max_thres = 30
    } else {
        max_thres = thresholds.rows[9].cells[1].innerHTML
        min_thres = thresholds.rows[8].cells[1].innerHTML
    }
    var bmi_max = parseInt(max_thres, 10) + 6
    var bmi_min = parseInt(min_thres, 10) - 6
    bmi_label.push(day)
    bmi.push(value)
    bmi_maxthres.push(max_thres)
    bmi_minthres.push(min_thres)
};


//SBP
for (var i = 0; i < sbp_table.rows.length; i++) {
    var day = sbp_table.rows[i].cells[0].innerHTML
    var value = sbp_table.rows[i].cells[1].innerHTML
    if (thresholds == null) {
        var min_thres = 110
        var max_thres = 130
    } else {
        max_thres = thresholds.rows[5].cells[1].innerHTML
        min_thres = thresholds.rows[4].cells[1].innerHTML
    }
    var sbp_max = parseInt(max_thres, 10) + 40
    var sbp_min = parseInt(min_thres, 10) - 40
    sbp_label.push(day)
    sbp.push(value)
    sbp_maxthres.push(max_thres)
    sbp_minthres.push(min_thres)
};


//DBP
for (var i = 0; i < dbp_table.rows.length; i++) {
    var day = dbp_table.rows[i].cells[0].innerHTML
    var value = dbp_table.rows[i].cells[1].innerHTML
    if (thresholds == null) {
        var min_thres = 70
        var max_thres = 90
    } else {
        max_thres = thresholds.rows[7].cells[1].innerHTML
        min_thres = thresholds.rows[6].cells[1].innerHTML
    }
    var dbp_max = parseInt(max_thres, 10) + 40
    var dbp_min = parseInt(min_thres, 10) - 40
    dbp_label.push(day)
    dbp.push(value)
    dbp_maxthres.push(max_thres)
    dbp_minthres.push(min_thres)
};

//CALORIES
for (var i = 0; i < cal_table.rows.length; i++) {
    var day = cal_table.rows[i].cells[0].innerHTML
    var value = cal_table.rows[i].cells[1].innerHTML
    if (thresholds == null) {
        var min_thres = 1200
        var max_thres = 3000
    } else {
        max_thres = thresholds.rows[19].cells[1].innerHTML
        min_thres = thresholds.rows[18].cells[1].innerHTML
    }
    var cal_max = parseInt(max_thres, 10) + 500
    var cal_min = parseInt(min_thres, 10) - 500
    cal_label.push(day)
    cal.push(value)
    cal_minthres.push(min_thres)
    cal_maxthres.push(max_thres)
};

//ACTIVITY 
for (var i = 0; i < act_table.rows.length; i++) {
    var day = act_table.rows[i].cells[0].innerHTML
    var value = act_table.rows[i].cells[1].innerHTML
    if (thresholds == null) {
        var min_thres = 1
    } else {
        min_thres = thresholds.rows[10].cells[1].innerHTML
    }
    var act_min = parseInt(min_thres, 10) - 2
    act_label.push(day)
    act.push(value)
    act_minthres.push(min_thres)
};

//PSQI
for (var i = 0; i < psq_table.rows.length; i++) {
    var day = psq_table.rows[i].cells[0].innerHTML
    var value = psq_table.rows[i].cells[1].innerHTML
    if (thresholds == null) {
        var min_thres = 0
        var max_thres = 21
    } else {
        max_thres = thresholds.rows[15].cells[1].innerHTML
        min_thres = thresholds.rows[14].cells[1].innerHTML
    }
    var psq_max = parseInt(max_thres, 10) + 6
    var psq_min = parseInt(min_thres, 10) - 6
    psq_label.push(day)
    psq.push(value)
    psq_minthres.push(min_thres)
};

//SLEEP QUALITY 
for (var i = 0; i < qua_table.rows.length; i++) {
    var day = qua_table.rows[i].cells[0].innerHTML
    var value = qua_table.rows[i].cells[1].innerHTML
    qua_label.push(day)
    qua.push(value)
};

//SLEEP EFFICIENCY
for (var i = 0; i < eff_table.rows.length; i++) {
    var day = eff_table.rows[i].cells[0].innerHTML
    var value = eff_table.rows[i].cells[1].innerHTML
    if (thresholds == null) {
        var min_thres = 0
        var max_thres = 100
    } else {
        max_thres = thresholds.rows[17].cells[1].innerHTML
        min_thres = thresholds.rows[16].cells[1].innerHTML
    }
    var eff_max = parseInt(max_thres, 10) + 20
    var eff_min = parseInt(min_thres, 10) - 20
    eff_label.push(day)
    eff.push(value)
    eff_minthres.push(min_thres)
};

//STRESS LEVEL
for (var i = 0; i < psl_table.rows.length; i++) {
    var day = psl_table.rows[i].cells[0].innerHTML
    var value = psl_table.rows[i].cells[1].innerHTML
    if (thresholds == null) {
        var min_thres = 0
        var max_thres = 40
    } else {
        max_thres = thresholds.rows[13].cells[1].innerHTML
        min_thres = thresholds.rows[12].cells[1].innerHTML
    }
    var psl_max = parseInt(max_thres, 10) + 20
    var psl_min = parseInt(min_thres, 10) - 20
    psl_label.push(day)
    psl.push(value)
    psl_minthres.push(min_thres)
    psl_maxthres.push(min_thres)
};

//--------------------PLOT----------------------------------------------
var ctx = document.getElementById('parametersChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',
    // The data for our dataset
    data: {},
    // Configuration options go here
    options: {}
});

/* function removeData(chart, data) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        for(var i=0; i < chart.data.length; i ++){
        dataset.data[i].pop();
        console.log(chart.data);
        }
    });
    chart.update();
}

 function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        for(var i=0; i < chart.data.length; i ++){
        dataset.data[i].push(data[i]);}
    });
    chart.update();
}*/


//BUTTON CODE: Charts to be updated based on the value given by the user
window.onload = function () {

    $("#graphtype").change(function () {
        console.log(id);
        // Food Calories-------------------------------------------
        if ($(this).val() == "F") {
            chart.data.labels = cal_label;
            chart.data.datasets = [{
                    label: 'kcal',
                    data: cal,
                    backgroundColor: 'rgba(198,21,21,0.5)',
                    borderColor: 'rgba(198,21,21,1.0)',
                },
                {
                    data: cal_minthres,
                    label: 'kcal minimum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(255,202,79,0.0)',
                    borderColor: 'rgba(198,21,21,1.0)',
      },
                {
                    data: cal_maxthres,
                    label: 'kcal maximum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(255,202,79,0.0)',
                    borderColor: 'rgba(198,21,21,1.0)',
      }, ];
            chart.options = {
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: "kcal",
                        },
                        display: true,
                        ticks: {
                            min: cal_min,
                            max: cal_max,
                            stepSize: 250
                        }
                        }],

                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: id,
                        }
                }]
                }
            }


        }

        // Blood Pressure-------------------------------------------
        if ($(this).val() == "DB") {
            chart.data.labels = dbp_label;
            chart.data.datasets = [
                {
                    data: sbp_minthres,
                    label: 'SBP minimum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(255,91,54,0.0)',
                    borderColor: 'rgba(255,91,54,1.0)',
      }, {
                    data: dbp_minthres,
                    label: 'DBP minimum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(255,91,54,0.0)',
                    borderColor: 'rgba(61,124,235,1.0)',
      },
                {
                    data: sbp_maxthres,
                    label: 'SBP maximum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(255,91,54,0.0)',
                    borderColor: 'rgba(255,91,54,1.0)',
      }, {
                    data: dbp_maxthres,
                    label: 'DBP maximum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(255,91,54,0.0)',
                    borderColor: 'rgba(61,124,235,1.0)',
      }, {
                    label: 'Dyastolic Blood Pressure',
                    data: dbp,
                    backgroundColor: 'rgba(116,159,255,0.5)',
                    borderColor: 'rgba(116,159,255,0.5)',
      }, {
                    label: 'Systolic Blood Pressure',
                    data: sbp,
                    backgroundColor: 'rgba(255,91,54,0.5)',
                    borderColor: 'rgba(255,91,54,0.5)',
      }];
            chart.options = {
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: "mmHg",
                        },
                        display: true,
                        ticks: {
                            min: dbp_min,
                            max: sbp_max,
                            stepSize: 20
                        }
      }],

                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: id,
                        }
                }]
                },
            };
        }

        // BMI-------------------------------------------
        if ($(this).val() == "W") {
            chart.data.labels = bmi_label;
            chart.data.datasets = [{
                    label: 'Body Mass Index',
                    data: bmi,
                    backgroundColor: 'rgba(255,165,20,0.5)',
                    borderColor: 'rgba(255,165,20,1.0)',
      },
                {
                    data: bmi_minthres,
                    label: 'BMI minimum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(66,129,255,0.0)',
                    borderColor: 'rgba(255,165,20,1.0)',
      },
                {
                    data: bmi_maxthres,
                    label: 'BMI maximum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(66,129,255,0.0)',
                    borderColor: 'rgba(255,165,20,1.0)',
      }];
            chart.options = {
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: "kg/m²",
                        },
                        display: true,
                        ticks: {
                            min: bmi_max,
                            max: bmi_min,
                            stepSize: 3,
                        }
                        }],

                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: id,
                        }
                }]
                }
            };
        }

        //Heart Rate-------------------------------------------
        if ($(this).val() == "H") {
            chart.data.labels = hr_label;
            chart.data.datasets = [{
                    label: 'Heart Rate',
                    data: hr,
                    backgroundColor: 'rgba(255,194,18,0.5)',
                    borderColor: 'rgba(255,194,18,1.0)',
      },
                {
                    data: hr_minthres,
                    label: 'HR minimum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(49,232,154,0.0)',
                    borderColor: 'rgba(215,154,0,1.0)',
      },
                {
                    data: hr_maxthres,
                    label: 'HR maximum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(49,232,154,0.0)',
                    borderColor: 'rgba(215,154,0,1.0)',
      }];
            chart.options = {
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: "bpm",
                        },
                        display: true,
                        ticks: {
                            min: hr_min,
                            max: hr_max,
                            stepSize: 10
                        }
      }],

                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: id,
                        }
                }]
                },
            }
        }

        //Physical Act-------------------------------------------
        if ($(this).val() == "O") {
            chart.data.labels = act_label;
            chart.data.datasets = [{
                    label: 'Physical Activity',
                    data: act,
                    backgroundColor: 'rgba(146,219,39,0.5)',
                    borderColor: 'rgba(146,219,39,1.0)',
      },
                {
                    data: act_minthres,
                    label: 'Hrs of act minimum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(49,232,154,0.0)',
                    borderColor: 'rgba(146,219,39,1.0)',
      }];
            chart.options = {
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: "HRS",
                        },
                        display: true,
                        ticks: {
                            min: 0,
                            stepSize: 1
                        }
      }],

                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: id,
                        }
                }]
                },
            }
        }

        //PSQI test-------------------------------------------
        if ($(this).val() == "P") {
            chart.data.labels = psq_label;
            chart.data.datasets = [{
                    label: 'PSQI',
                    data: psq,
                    backgroundColor: 'rgba(0,240,136,0.5)',
                    borderColor: 'rgba(0,240,136,1.0)',
      },
                {
                    data: psq_minthres,
                    label: 'PSQI minimum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(49,232,154,0.0)',
                    borderColor: 'rgba(0,240,136,1.0)',
      }];
            chart.options = {
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: " ",
                        },
                        display: true,
                        ticks: {
                            min: 0,
                            max: 21,
                            stepSize: 3
                        }
                        }],

                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: id,
                        }
                }]
                }
            };
        }

        //Sleep Quality-------------------------------------------
        if ($(this).val() == "S") {
            chart.data.labels = qua_label;
            chart.data.datasets = [{
                    label: 'Subjective SQ',
                    data: qua,
                    backgroundColor: 'rgba(49,179,172,0.5)',
                    borderColor: 'rgba(49,179,172,1.0)',
      },
                {
                    data: qua_minthres,
                    label: 'Subjective SQ minimum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(49,179,172,0.0)',
                    borderColor: 'rgba(49,179,172,1.0)',
      }];
            chart.options = {
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: " ",
                        },
                        display: true,
                        ticks: {
                            min: 0,
                            max: 5,
                            stepSize: 1
                        }
                        }],

                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: id,
                        }
                }]
                }
            };
        }

        // Sleep Efficiency-------------------------------------------
        if ($(this).val() == "E") {
            chart.data.labels = eff_label;
            chart.data.datasets = [{
                    label: 'Sleep Efficiency',
                    data: eff,
                    backgroundColor: 'rgba(165,50,250,0.5)',
                    borderColor: 'rgba(165,50,250,1.0)',
      },
                {
                    data: eff_minthres,
                    label: 'Sleep Efficiency minimum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(49,179,172,0.0)',
                    borderColor: 'rgba(165,50,250,1.0)',
      }];
            chart.options = {
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: " ",
                        },
                        display: true,
                        ticks: {
                            min: 0,
                            max: 100,
                            stepSize: 10,
                        }
                        }],

                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: id,
                        }
                }]
                }
            };
        }

        // Stress Level------------------------------------------
        if ($(this).val() == "SL") {
            chart.data.labels = psl_label;
            chart.data.datasets = [{
                    label: 'Perceived stress level',
                    data: psl,
                    backgroundColor: 'rgba(220,145,200,0.5)',
                    borderColor: 'rgba(220,145,200,1.0)',
      },
                {
                    data: psl_minthres,
                    label: 'Perceived stress level minimum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(49,179,172,0.0)',
                    borderColor: 'rgba(220,145,200,1.0)',
      },
                {
                    data: psl_maxthres,
                    label: 'Perceived stress level maximum threshold',
                    radius: 0,
                    borderWidth: 1,
                    borderDash: [5, 15],
                    backgroundColor: 'rgba(49,179,172,0.0)',
                    borderColor: 'rgba(220,145,200,1.0)',
      }];
            chart.options = {
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: " ",
                        },
                        display: true,
                        ticks: {
                            min: 0,
                            max: 40,
                            stepSize: 5,
                        }
                        }],

                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: id,
                        }
                }]
                }
            };
        }

        //-------------------------------------------
        chart.update();
    });

    $("#graphtype").trigger("change");
}









$('#update').click(function () {
    // $("#graph-container").css("display","block");
    var beg = $('#datetimepicker12').data("datetimepicker").date().format('L');
    var end = $('#datetimepicker13').data("datetimepicker").date().format('L');
    var dates = [beg, end]
    document.getElementById("update").value = dates;
    console.log(dates);
});
