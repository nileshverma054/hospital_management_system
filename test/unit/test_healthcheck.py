from test.unit.test_factory import TestFactory


class TestHealthcheck(TestFactory):
    def test_healthcheck(self):
        response = self.app.get("/api/v1/healthcheck")
        self.assertEqual(response.status_code, 204)
