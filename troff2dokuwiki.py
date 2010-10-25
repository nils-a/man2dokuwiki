#/usr/bin/env python
# -*- Encoding: UTF-8 -*-
#Trying to make a nice DokuWiki page from 
# a man-page.
# The first goal is to parse the manpage for xfreerdp 
# from freerdp project (www.freerdp.com)
# 2010 Nils Andresen nils@nils-andresen.de

from sys import argv,stderr,stdout

debug = True

def WikiSave(text):
	if text.startswith('"') and text.endswith('"'):
		text = text[1:-1]
	text = text.replace('[[', '%%[[%%')
	text = text.replace(']]', '%%]]%%')
	text = text.replace('\\-', '-')
	return text

def ParseLines(stack):
	while len(stack) > 0:
		line = stack.pop()
		if line.startswith('.TH'):
			# .TH title section [extra1... 
			# Titel ..
			line = line[4:]
			if debug:
				stderr.write('- Parsed as title: >%s<\n' % line)
			(title, section, _) = line.split(' ', 2)
			stdout.write(' ====== %s (%s) ======\n' % (WikiSave(title), section))
		elif line.startswith('.SH'):
			# Set up an unnumbered section heading
			title = line[4:]
			if title.strip() == '':
				title = stack.pop()
			if debug:
				stderr.write('- Parsed as section: >%s<\n' % line)
			stdout.write(' ===== %s =====\n' % WikiSave(title))
		elif line.startswith('.TP'):
			# Set up an indented paragraph with label
			line = line[4:]
			if not line.strip() == '':
				stderr.write('NOT-IMPLEMENTED: Indetion by >%s<\n' % line) 
			title = stack.pop()
			if title.startswith('.'):
				# This is mainly bold, but we don't need that here...
				(_, title) = title.split(' ', 1)
			if debug:
				stderr.write('- Parsed as paragraph: >%s<\n' %  title)
			stdout.write(' === %s ===\n' % WikiSave(title))
		elif line.startswith('.LP')  or line.startswith('.PP')  or line.startswith('.P'):
			# Any of them causes a line break at the current position and resets...
			if debug:
				stderr.write('- Parsed a break and reset: >%s<\n' % line)
			stdout.write('\n')			
		elif line.startswith('.I'):
			line = line[3:]
			if line.strip() == '':
				line = stack.pop()
			if debug:
				stderr.write('- Parsed as italic: >%s<\n' % line)
			stdout.write('//%s// ' % WikiSave(line))
		elif line.startswith('.B'):
			line = line[3:]
			if line.strip() == '':
				line = stack.pop()
			if debug:
				stderr.write('- Parsed as bold: >%s<\n' % line)
			stdout.write('**%s** ' % WikiSave(line))
		elif line.startswith('.br'):
			if debug:
				stderr.write('- Parsed a break: >%s<\n' % line)
			stdout.write('\n')
		elif line.startswith('\\fI'):
			#this is a wild guess - I found no documentation on this one...
			line = line[3:]
			if debug:
				stderr.write('- Parsed as link: >%s<\n' % line)
			stdout.write('[[%s]] ' % WikiSave(line))			
		elif line.strip() == '':
			stdout.write('\n')
		elif not line.startswith('.'):
			stdout.write('%s\n' % WikiSave(line))
		else:
			stderr.write('Unknown: %s\n' % line) 

def ReadFile(fileName):
	lines = []
	file = open(fileName, 'r')
	for line in file:
		lines.append(line[0:-1])
	file.close
	return lines

def main():
	lineList = ReadFile(argv[1])	
	lineList.reverse()
	ParseLines(lineList)
	
if __name__ == '__main__':
	main()