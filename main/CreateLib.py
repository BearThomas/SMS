import LibC

file = LibC.Lib(r'C:\Users\thomas\Documents\GitHub\SMS\main\Date\Students.xLib')

file.crTabel("Students", ['Name', 'Age', 'Birthday', 'Group', 'Num', 'Score'])
file.crTabel("Groups", ['Name', 'Score', 'Head', 'Member'])

file.table("Students").add(['xxx', 13, 20120403, 1, 38, 100])
file.table("Students").add(['xxx2', 13, 20120403, 1, 39, 100])

print(file.table("Students").data)

file.save()
file.close()

file_other = LibC.Lib('./main/Date/Other.xLib')

file_other.crTabel("Announcements", ['Time', 'Note', 'People'])
file_other.crTabel("Lessons", ['Time', 'Subject', 'Note', 'Teacher'])
file_other.crTabel("Homework", ['Date', 'Note', 'Subject'])
file_other.crTabel("Log", ['Time', 'Type', 'Note'])

file_other.save()
