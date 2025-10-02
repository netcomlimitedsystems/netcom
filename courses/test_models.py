import pytest
from courses.models import Course

@pytest.mark.django_db
def test_course_str():
    course = Course.objects.create(title="Cybersecurity Basics", description="Intro")
    assert str(course) == "Cybersecurity Basics"
