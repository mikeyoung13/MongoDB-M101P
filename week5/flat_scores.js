use agg
db.scores.drop()
var types = ['exam', 'quiz', 'homework', 'homework'];
// 50 students
for (var i = 0; i < 50; i++) {
    // print("working on student", i);
    // take between 1 .. 10 classes
    var num_classes = Math.floor(Math.random()*11);
    for (class = 0; class < num_classes; class++) {
	// there are 500 different classes that they can take
	class_id = Math.floor(Math.random()*501); // get a class id between 0 and 500

	    // and each class has 4 grades
	    for (j = 0; j < 4; j++) {
		
		record = {'student_id':i, 'class_id':class_id,
			  'type':types[j],'score':Math.random()*100};
		db.grades.insert(record);
	    }

    }
}

	    
