def linear_interpolation(vec1, vec2, koeff):
	return vec1 + (vec2 - vec1).scale(koeff)