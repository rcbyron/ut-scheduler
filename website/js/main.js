
var BASE_URL = "http://ut-scheduler.us-west-1.elasticbeanstalk.com/"; //"http://127.0.0.1:8000/";
var BASE_DATES = {
    M: '2017-01-02T',
    T: '2017-01-03T',
    W: '2017-01-04T',
    R: '2017-01-05T',
    F: '2017-01-06T'
};
var MAJOR_CHOICES = [
    "ACC - Accounting",
    "ADV - Advertising",
    "ASE - Aerospace Engineering",
    "AFR - African & African Diaspora Std",
    "AFS - Air Force Science",
    "ASL - American Sign Language",
    "AMS - American Studies",
    "AHC - Ancient Hist and Classical Civ",
    "ANT - Anthropology",
    "ALD - Applied Learning & Development",
    "ARA - Arabic",
    "ARE - Architectural Engineering",
    "ARI - Architectural Interior Design",
    "ARC - Architecture",
    "AED - Art Education",
    "ARH - Art History",
    "ART - Art, Studio",
    "AET - Arts and Entertainment Technologies",
    "AAS - Asian American Studies",
    "ANS - Asian Studies",
    "AST - Astronomy",
    "BSN - Bassoon",
    "BEN - Bengali",
    "BCH - Biochemistry",
    "BIO - Biology",
    "BME - Biomedical Engineering",
    "BDP - Bridging Disciplines",
    "B A - Business Administration",
    "BGS - Business, Govt, and Society",
    "CHE - Chemical Engineering",
    "CH  - Chemistry",
    "CHI - Chinese",
    "C E - Civil Engineering",
    "CLA - Clarinet",
    "C C - Classical Civilization",
    "CGS - Cognitive Science",
    "CSD - Comm Sciences and Disorders",
    "COM - Communication",
    "CMS - Communication Studies",
    "CRP - Community & Regional Planning",
    "C L - Comparative Literature",
    "COE - Computational Engineering",
    "CSE - Computatnl Sci, Engr, and Math",
    "C S - Computer Science",
    "CON - Conducting",
    "CTI - Core Texts and Ideas",
    "CRW - Creative Writing",
    "EDC - Curriculum and Instruction",
    "CZ  - Czech",
    "DAN - Danish",
    "DES - Design",
    "DEV - Developmental Studies",
    "D B - Double Bass",
    "DRS - Drum Set",
    "DCH - Dutch",
    "ECO - Economics",
    "EDA - Educational Administration",
    "EDP - Educational Psychology",
    "E E - Electrical & Computer Engr",
    "EER - Energy and Earth Resources",
    "ENM - Engineering Management",
    "E M - Engineering Mechanics",
    "E S - Engineering Studies",
    "E   - English",
    "ESL - English As A Second Language",
    "ENS - Ensemble",
    "EVE - Environmental Engineering",
    "EVS - Environmental Science",
    "EUP - Euphonium",
    "EUS - European Studies",
    "FIN - Finance",
    "F A - Fine Arts",
    "FLU - Flute",
    "FLE - Foreign Language Education",
    "FR  - French",
    "F C - French Civilization",
    "F H - French Horn",
    "G E - General Engineering",
    "GRG - Geography",
    "GEO - Geological Sciences",
    "GER - German",
    "GSD - German, Scandinavian, and Dutch",
    "GOV - Government",
    "GK  - Greek",
    "GUI - Guitar",
    "HAR - Harp",
    "H S - Health and Society",
    "HED - Health Education",
    "HEB - Hebrew",
    "HIN - Hindi",
    "HIS - History",
    "HDF - Human Dev and Family Sciences",
    "HDO - Human Dimensions of Orgs",
    "HMN - Humanities",
    "ILA - Iberian & Lat Amer Lang & Cult",
    "IMS - Identity Management and Security",
    "INF - Information Studies",
    "I B - International Business",
    "IRG - Intl Rels and Global Studies",
    "ISL - Islamic Studies",
    "ITL - Italian",
    "ITC - Italian Civilization",
    "JPN - Japanese",
    "J S - Jewish Studies",
    "J   - Journalism",
    "KIN - Kinesiology",
    "KOR - Korean",
    "LAR - Landscape Architecture",
    "LAT - Latin",
    "LAL - Latin American Languages, Indigenous",
    "LAS - Latin American Studies",
    "LAW - Law",
    "LEB - Legal Environment of Business",
    "L A - Liberal Arts",
    "LAH - Liberal Arts Honors",
    "LIN - Linguistics",
    "MAL - Malayalam",
    "MAN - Management",
    "MIS - Management Information Systems",
    "MFG - Manufacturing Sys Engineering",
    "MNS - Marine Science",
    "MKT - Marketing",
    "MSE - Materials Science & Engr",
    "M   - Mathematics",
    "M E - Mechanical Engineering",
    "MDV - Medieval Studies",
    "MAS - Mexican American Studies",
    "MEL - Middle Eastern Langs and Culs",
    "MES - Middle Eastern Studies",
    "M S - Military Science",
    "MOL - Molecular Biology",
    "MUS - Music",
    "MBU - Music Business",
    "MRT - Music Recording Technology",
    "NSC - Natural Sciences",
    "N S - Naval Science",
    "NEU - Neuroscience",
    "NOR - Norwegian",
    "N   - Nursing",
    "NTR - Nutrition",
    "OBO - Oboe",
    "OPR - Opera",
    "O M - Operations Management",
    "ORI - Operations Rsch & Indstrl Engr",
    "ORG - Organ",
    "PER - Percussion",
    "PRS - Persian",
    "PGE - Petroleum & Geosystems Engr",
    "PGS - Pharmacy Graduate Studies",
    "PHM - Pharmacy Pharmd",
    "PHL - Philosophy",
    "PED - Physical Education",
    "P S - Physical Science",
    "PHY - Physics",
    "PIA - Piano",
    "POL - Polish",
    "POR - Portuguese",
    "PRC - Portuguese Civilization",
    "PSY - Psychology",
    "P A - Public Affairs",
    "PBH - Public Health",
    "P R - Public Relations",
    "RTF - Radio-Television-Film",
    "R E - Real Estate",
    "R S - Religious Studies",
    "RHE - Rhetoric and Writing",
    "R M - Risk Management",
    "REE - Rus, East Eur, & Eurasian Stds",
    "RUS - Russian",
    "SAN - Sanskrit",
    "SAX - Saxophone",
    "STC - Sci & Tech Commercialization",
    "STM - Sci/Tech/Engineering/Math Educ",
    "S C - Serbian/Croatian",
    "SEL - Slavic Languages and Culture",
    "S S - Social Science",
    "S W - Social Work",
    "SOC - Sociology",
    "SPN - Spanish",
    "SPC - Spanish Civilization",
    "SED - Special Education",
    "STA - Statistics",
    "SDS - Statistics and Data Sciences",
    "SWE - Swedish",
    "TAM - Tamil",
    "TEL - Telugu",
    "TXA - Textiles and Apparel",
    "T D - Theatre and Dance",
    "TRO - Trombone",
    "TRU - Trumpet",
    "TBA - Tuba",
    "TUR - Turkish",
    "T C - Tutorial Course",
    "UGS - Undergraduate Studies",
    "URB - Urban Studies",
    "URD - Urdu",
    "UTL - UTeach-Liberal Arts",
    "UTS - UTeach-Natural Sciences",
    "VIA - Viola",
    "VIO - Violin",
    "V C - Violoncello",
    "VAS - Visual Art Studies",
    "VOI - Voice",
    "WGS - Women's and Gender Studies",
    "WRT - Writing",
    "YID - Yiddish",
    "YOR - Yoruba"
];
var TIMES = {
    14: "7:00 AM",
    15: "7:30 AM",
    16: "8:00 AM",
    17: "8:30 AM",
    18: "9:00 AM",
    19: "9:30 AM",
    20: "10:00 AM",
    21: "10:30 AM",
    22: "11:00 AM",
    23: "11:30 AM",
    24: "12:00 AM",
    25: "12:30 AM",
    26: "1:00 PM",
    27: "1:30 PM",
    28: "2:00 PM",
    29: "2:30 PM",
    30: "3:00 PM",
    31: "3:30 PM",
    32: "4:00 PM",
    33: "4:30 PM",
    34: "5:00 PM",
    35: "5:30 PM",
    36: "6:00 PM",
    37: "6:30 PM",
    38: "7:00 PM",
    39: "7:30 PM",
    40: "8:00 PM",
    41: "8:30 PM",
    42: "9:00 PM",
    43: "9:30 PM",
    44: "10:00 PM",
};

var courses = {};
var generated_schedules = [];
var available_schedules = [];
var selectedCourses = [];
var scheduleIndex = 0;
var slider;

function UTClass(obj) {
    /* Wraps a JSON UT class object */
    this.getRandomColor = function() {
        /* Gets a random dark color */
        var letters = '0123456789'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++)
            color += letters[Math.floor(Math.random() * letters.length)];
        return color;
    }

    this.addSections = function (days, startTime, endTime) {
        for (var z = 0; z < days.length; z++) {
            var sectionStart = moment.utc(BASE_DATES[days[z]]+startTime.format(" HH:mm"), 'YYYY-MM-DD HH:mm');
            var sectionEnd = moment.utc(BASE_DATES[days[z]]+endTime.format(" HH:mm"), 'YYYY-MM-DD HH:mm');
            this.sections.push({
                title: this.unique.toString() + " - " + this.courseName,
                start: sectionStart.toISOString(),
                end: sectionEnd.toISOString(),
                color: this.uniqueColor
            });
        }
    };

    this.unique = obj['unique'];
    this.courseName = courses[obj['course_id']].name;

    this.sections = [];
    this.uniqueColor = this.getRandomColor();
    this.days1 = (obj.days1 == null ? [] : obj.days1.replace(/TH/g, 'R').split(''));
    this.days2 = (obj.days2 == null ? [] : obj.days2.replace(/TH/g, 'R').split(''));
    this.startTime1 = moment(obj['start_time1'], "HH:mm:ss");
    this.endTime1   = moment(obj['end_time1'], "HH:mm:ss");
    this.startTime2 = moment(obj['start_time2'], "HH:mm:ss");
    this.endTime2   = moment(obj['end_time2'], "HH:mm:ss");

    if (this.days1.length > 0) { this.addSections(this.days1, this.startTime1, this.endTime1); }
    if (this.days2.length > 0) { this.addSections(this.days2, this.startTime2, this.endTime2); }
}


function addCourse() {
    /* Adds a course to the selected list and updates the HTML course display */
    console.log("Adding selected course:", $('#courses').val());
    if (selectedCourses.indexOf($('#courses').val()) == -1) {  // course not already in selected list
        selectedCourses.push($('#courses').val());

        // Clear and update HTML list of courses
        var htmlCourses = "";
        for (var i in selectedCourses)
            htmlCourses += "<li><span>" + courses[selectedCourses[i]].name + "</span><i class=\"fa fa-trash\"></i></li>";
        $("#selected-courses").html(htmlCourses);

    } else
        console.log("Duplicate course");
}


function clearCourses() {
    /* Clear selected courses and remove them from the HTML */
    selectedCourses = [];
    $("#selected-courses").html("");
    $('#calendar').fullCalendar('removeEvents');
}


function showNextSchedule() {
    /* Show the next possible schedule */
    displaySchedule(available_schedules[(scheduleIndex++) % available_schedules.length]);
}

function displaySchedule(classes) {
    // Remove previously displayed schedule
    $('#calendar').fullCalendar('removeEvents');

    var minTime = moment('23:59:59', 'HH:mm:ss');
    var maxTime = moment('00:00:00', 'HH:mm:ss');

    for (var i in classes) {
        var t1 = classes[i].startTime1;
        var t2 = classes[i].startTime2;
        var t3 = classes[i].endTime1;
        var t4 = classes[i].endTime2;
        if (t1 < minTime) minTime = t1;
        if (t2 < minTime) minTime = t2;
        if (t3 > maxTime) maxTime = t3;
        if (t4 > maxTime) maxTime = t4;

        for (var j in classes[i].sections) {
            $('#calendar').fullCalendar('renderEvent', classes[i].sections[j], true);

            if ($('.fc-time-grid-event').length > 0) {
                var renderedEvents = $('div.fc-event-container a');
                var firstEventOffsetTop = renderedEvents && renderedEvents.length > 0 ? renderedEvents[0].offsetTop : 0;
                $('div.fc-scroller').animate({
                    scrollTop: firstEventOffsetTop
                }, 200);
            }
        }
    }

    // add some padding above the earliest class and below the latest class
    minTime.subtract(30, 'minutes');
    maxTime = maxTime.add(30, 'minutes');

    $('#calendar').fullCalendar('option', 'minTime', minTime.format("HH:mm:ss"));
    $('#calendar').fullCalendar('option', 'maxTime', maxTime.format("HH:mm:ss"));
}

function generateSchedules() {
    /* Send course IDs to API to generate schedules */
    console.log("Selected Course IDs:", selectedCourses);
    $.ajax({
        type: "POST",
        url: BASE_URL + "schedules",
        data: JSON.stringify(selectedCourses),
        dataType: "json",
        success: function (data) {
            generated_schedules = data;
            scheduleIndex = 0;
            updateScheduleConstraints();
            showNextSchedule();
        }
    });
}

function arraysEqual(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (a.length != b.length) return false;

    for (var i = 0; i < a.length; ++i) {
        if (a[i] !== b[i]) return false;
    }
    return true;
}

function updateScheduleConstraints() {
    scheduleIndex = 0;
    available_schedules = jQuery.extend(true, {}, generated_schedules);
    for (var i = available_schedules.length - 1; i >= 0; i--) {
        console.log("Checking, ", available_schedules[i])
        for (var j in available_schedules[i]) {
            var utClass = new UTClass(available_schedules[i][j]);
            var timeVals = slider.slider('getValue');
            console.log(utClass, moment(TIMES[timeVals[0]], "hh:mm A"), utClass.startTime1 < moment(TIMES[timeVals[0]], "hh:mm A"))

            if ((utClass.startTime1 < moment(TIMES[timeVals[0]], "hh:mm A")) ||
                (utClass.startTime2 < moment(TIMES[timeVals[0]], "hh:mm A")) ||
                (utClass.endTime1 > moment(TIMES[timeVals[1]], "hh:mm A")) ||
                (utClass.endTime2 > moment(TIMES[timeVals[1]], "hh:mm A")))
                available_schedules[i]['isAvailable'] = false;
        }
        if (!isAvailable) available_schedules.splice(i, 1);
    }
    $('#number-generated').text("Schedules: " + available_schedules.length);
}

$(document).ready(function () {
    var cal = $('#calendar');
    cal.fullCalendar({
        header: false,
        defaultView: 'agendaWeek',
        defaultDate: '2017-01-01',
        allDaySlot: false,
        columnFormat: 'dddd',
        minTime: '07:00:00',
        maxTime: '22:00:00',
        editable: false,
        weekends: false,
    });
    if ($(window).width() < 480) $('#calendar').fullCalendar('option', 'columnFormat', 'ddd');
    $(window).resize(function() {
        var colFormat = ($(window).width() < 480) ? 'ddd' : 'dddd';
        $('#calendar').fullCalendar('option', 'columnFormat', colFormat);
    })

    slider = $("#time-slider").slider(
        {
            id: "time-slider",
            min: 14,  // 7:00 AM
            max: 44,  // 10:00 PM
            range: true,
            value: [14, 44],
            formatter: function (value) {
                return TIMES[value[0]] + " - " + TIMES[value[1]]
            }
        }
    );
    var originalVals;

    $("#time-slider").on("slideStart", function(slideEvt) {
        originalVals = slideEvt.value;
    });
    $("#time-slider").on("slideStop", function(slideEvt) {
        var newVals = slideEvt.value;
        if (!arraysEqual(originalVals, newVals)) {
            updateScheduleConstraints();
        }
    });

    function loadMajors() {
        /* Load fields of study into the selection box */
        var majors = $("#majors");
        majors.empty(); // remove old options
        for (var i in MAJOR_CHOICES) {
            var val = MAJOR_CHOICES[i].slice(0, 3).replace(/ /g, '');  // e.g. "ACC" or "EE"
            majors.append($("<option></option>").attr("value", val).text(MAJOR_CHOICES[i]));
        }
    }
    function updateCourses() {
        var url = BASE_URL + $('#majors').val() + "/courses";
        $.get(url, function (json_str) {
            var coursesObj = $("#courses");
            coursesObj.empty();

            courses = json_str;
            for (var key in courses) {
                coursesObj.append($("<option></option>").attr("value", key).text(courses[key].name));
            }
            coursesObj.selectpicker('refresh');
        });

    }
    loadMajors();
    updateCourses();
    document.getElementById('majors').onchange = updateCourses;

});
