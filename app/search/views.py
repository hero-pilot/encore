from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from elasticsearch_dsl import Q
from .documents import EventDocument
from .serializers import EventDocumentSerializer

class EventSearchView(APIView):
    """
    Search endpoint for Events backed by Elasticsearch.
    Example: GET /api/search/events/?q=rock&venue_id=1
    """
    permission_classes = [AllowAny] 

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')
        venue_id = request.query_params.get('venue_id', None)

        # 1. Initialize the Search object targeting the 'events' index
        search_query = EventDocument.search()

        # 2. Build Full-Text Search across multiple fields
        if query:
            search_query = search_query.query(
                "multi_match",
                query=query,
                fields=['title^3', 'description', 'performer_name^2', 'venue_location'],
                fuzziness="AUTO"  # Handles minor typos automatically
            )
        else:
            search_query = search_query.query("match_all")

        # 3. Add Exact Filters
        if venue_id:
            search_query = search_query.filter("term", venue_id=venue_id)

        # 4. Execute search and get results
        response = search_query.execute()

        # 5. Serialize hits
        # Note: 'hit.to_dict()' converts the Elasticsearch hit object into a Python dict
        results = [hit.to_dict() for hit in response]
        serializer = EventDocumentSerializer(results, many=True)

        return Response({
            "count": response.hits.total.value,
            "results": serializer.data
        }, status=status.HTTP_200_OK)