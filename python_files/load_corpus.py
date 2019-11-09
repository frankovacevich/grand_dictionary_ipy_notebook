from python_files.get_html import remove_shit

def load_corpus_summary(file_name, inverse_dict, balanced = True):

	corpus = {}
	corpus_original = {}
	corpus_count = 0
	corpus_original_count = 0

	with open(file_name,"r",encoding="UTF-8") as f:
		for line in f:
			line = line.replace("\n","").replace("(","").replace("(","").split(" ")
			word = remove_shit(line[0])
			
			if word == "" or word == " ":
				continue
			word = word.replace(" ","")

			count = int(line[1])
			
			## Add word to the original corpus (not filtered)
			corpus_original_count += count
			if word not in corpus_original:
				corpus_original[word] = 0
			corpus_original[word] += count
				
			## Add word to the filtered corpus (only words in the Grand Croatian Dict)
			corpus_count += count

			if word not in inverse_dict:
				continue
		
			for w in inverse_dict[word]:
				if w not in corpus:
					corpus[w] = 0
				corpus[w] += count
				
				if not balanced:
					break

		f.close()

	for item in corpus:
		corpus[item] = 1000 * corpus[item] / corpus_count
	for item in corpus_original:
		corpus_original[item] = 1000 * corpus_original[item] / corpus_count
		
	print("Loaded corpus from " + file_name + " (" + str(corpus_count/1E6) + "M words)")
	return {"corpus": corpus, "corpus_original": corpus_original, "count" : corpus_count, "count_original" : corpus_original_count}


def create_combined_corpus(list_of_corpuses):

	combined_corpus = {}

	list_of_words = []

	for corpus in list_of_corpuses:
		for key in corpus:
			if key not in list_of_words:
				list_of_words.append(key)

	for word in list_of_words:
		
		inverse_total = 0
		word_presence = True
		for corpus in list_of_corpuses:
			if word in corpus and corpus[word] != 0:
				inverse_total += 1 / corpus[word]
			else:
				word_presence = False
				break

		if word_presence:
			combined_corpus[word] = len(list_of_corpuses) / inverse_total
		else:
			combined_corpus[word] = 0

	print("Created combined corpus")
	return combined_corpus