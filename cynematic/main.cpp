#include <linalg.h>
#include <linalg-ext.h>

#include <iostream>
#include <vector>

#include <gxx/print.h>
#include <gxx/trace.h>

using namespace linalg;
using namespace linalg::aliases;
using namespace linalg::ostream_overloads;

double deg(double angle)
{
	return angle * M_PI / 180.0;
}

namespace cynematic
{
	struct abstract_link
	{
		virtual double4x4 get(const std::vector<double>& coords, uint8_t pos) = 0;
		virtual double4x4 sensmat() = 0;
		virtual uint8_t count_of_coords() = 0;
	};

	struct constant_link : public abstract_link
	{
		double4x4 mat;
		double4x4 get(const std::vector<double>& coords, uint8_t pos) override { return mat; }
		double4x4 sensmat() { return double4x4(); }
		uint8_t count_of_coords() override { return 0; }
		constant_link(double4x4 _mat) : mat(_mat) {};
	};

	template<typename F>
	struct one_dof_link_t : public abstract_link
	{
		F func;
		double4x4 get(const std::vector<double>& coords, uint8_t pos) override
		{
			return func(coords[pos]);
		}
		double4x4 sensmat() { return double4x4(); }
		uint8_t count_of_coords() override { return 1; }
		one_dof_link_t(F _func) : func(_func) {};
	};
	template <typename F>
	one_dof_link_t<F> one_dof_link(F func) { return one_dof_link_t<F>(func); }

	struct parametric_rotation_link : public abstract_link
	{
		double3 axvec;
		parametric_rotation_link(double3 _axvec) : axvec(_axvec) {}

		double4x4 get(const std::vector<double>& coords, uint8_t pos) override
		{
			return homogeneous_transformation<double, 3>::rotation( rotation_quat(axvec, coords[pos]) );
		}
		double4x4 sensmat() { //return homogeneous_transformation<double, 3>::rotation( rotation_quat(axvec, ) ); 
		}

		uint8_t count_of_coords() override { return 1; }
	};

	struct parametric_translation_link : public abstract_link
	{
		double3 axvec;
		parametric_translation_link(double3 _axvec) : axvec(_axvec) {}

		double4x4 get(const std::vector<double>& coords, uint8_t pos) override
		{
			return homogeneous_transformation<double, 3>::translation( axvec * coords[pos] );
		}
		double4x4 sensmat() { return homogeneous_transformation<double, 3>::translation( axvec ) - double4x4(identity); }

		uint8_t count_of_coords() override { return 1; }
	};

	struct chain
	{
		std::vector<abstract_link *> links;

		void add_link(abstract_link* lnk) { links.push_back(lnk); }

		double4x4 get(const std::vector<double>& coords)
		{
			double4x4 result = identity;
			int8_t coord_pos = coords.size() - 1;

			for (int i = links.size() - 1; i >= 0; --i)
			{
				uint8_t count_of_coords = links[i]->count_of_coords();

				if (coord_pos - count_of_coords + 1 < 0)
					return double4x4();

				double4x4 nmat = links[i]->get(coords, coord_pos);
				result = nmat * result;
				coord_pos -= count_of_coords;
			}

			return result;
		}

		std::vector<double4x4> sensivity_matrices(const std::vector<double>& coords)
		{
			TRACE();
			std::vector<double4x4> result;
			double4x4 curtrans = identity;
			int8_t coord_pos = coords.size() - 1;

			for (int i = links.size() - 1; i >= 0; --i)
			{
				uint8_t count_of_coords = links[i]->count_of_coords();

				if (coord_pos - count_of_coords + 1 < 0)
					return std::vector<double4x4>();

				if (count_of_coords > 0)
				{
					if (count_of_coords == 1)
					{
						auto sensmat = links[i]->sensmat();
						result.emplace_back(curtrans * sensmat);
					}
					else
					{
						return std::vector<double4x4>();
					}
				}

				double4x4 nmat = links[i]->get(coords, coord_pos);
				curtrans = nmat * curtrans;
						
				coord_pos -= count_of_coords;
			}

			return result;

		}

		std::vector<double> sensivity(std::vector<double> curcoords, double4x4 target)
		{
			auto curmat = get(curcoords);
			auto needmat = target * inverse(curmat);

			auto sensmats = sensivity_matrices(curcoords);

			std::cout << "needmat: " << needmat << std::endl;
			for (auto m : sensmats) {
				std::cout << "smat: " << m << std::endl;
			}
		}
	};

	struct dynamic_chain : public chain
	{
		~dynamic_chain()
		{
			for (int i = 0; i < links.size(); ++i) delete links[i];
		}
	};
}

int main ()
{
	cynematic::chain chain;

	auto link2 = cynematic::one_dof_link(
	                 [](double coord)
	{
		return homogeneous_transformation<double, 3>::rotation( rotation_quat(double3(0, 1, 0), coord) );
	}
	             );

	mat<double, 4, 4> m;
	m[0].x;

	std::cout << m;

	chain.add_link(new cynematic::constant_link(
	                   homogeneous_transformation<double, 3>::translation(double3(5, 0, 5))
	               ));
	chain.add_link(new cynematic::parametric_translation_link(double3(0, 0, 1)));
	chain.add_link(new cynematic::parametric_rotation_link(double3(0, 0, 1)));
	chain.add_link(&link2);

	auto result = chain.get({0, deg(0), deg(0)});

	auto sens = chain.sensivity({0, deg(0), deg(0)},
	                            homogeneous_transformation<double, 3>::pose(
	                                rotation_quat( double3(0, 0, 1), 0.0 ),
	                                double3(5, 0, 10)
	                            )
	                           );
}