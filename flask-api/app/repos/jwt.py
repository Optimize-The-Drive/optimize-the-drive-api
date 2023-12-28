
from app.models.jwt import JWT
from .base import BaseRepo

class JWTRepo(BaseRepo):
	'''
		JWTRepo defintion. Extends the BaseRepository.

		methods:
			by_jti
	'''
	def by_jti(self, jti: str) -> JWT:
		'''
			Queries a JWT token by it's JTI.

			arguments:
				jti: str
			returns: JWT
		'''
		return self._db.session.execute(
			self._db.select(JWT).filter_by(jti=jti)
		).scalar()
