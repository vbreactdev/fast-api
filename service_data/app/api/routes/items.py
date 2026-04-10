from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_current_principal, get_item_repository
from app.schemas.data import ItemCreate, ItemListResponse, ItemResponse, Principal
from app.services.repository import InMemoryItemRepository

router = APIRouter(prefix="/api/v1/items", tags=["items"])


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item for the authenticated subject",
)
async def create_item(
    payload: ItemCreate,
    principal: Principal = Depends(get_current_principal),
    repository: InMemoryItemRepository = Depends(get_item_repository),
) -> ItemResponse:
    return await repository.create_item(payload=payload, owner=principal.subject)


@router.get(
    "",
    response_model=ItemListResponse,
    summary="List items owned by the authenticated subject",
)
async def list_items(
    principal: Principal = Depends(get_current_principal),
    repository: InMemoryItemRepository = Depends(get_item_repository),
) -> ItemListResponse:
    items = await repository.list_items(owner=principal.subject)
    return ItemListResponse(items=items, count=len(items))


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get a single item owned by the authenticated subject",
)
async def get_item(
    item_id: str,
    principal: Principal = Depends(get_current_principal),
    repository: InMemoryItemRepository = Depends(get_item_repository),
) -> ItemResponse:
    item = await repository.get_item(item_id=item_id)
    if item is None or item.owner != principal.subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )
    return item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single item owned by the authenticated subject",
)
async def delete_item(
    item_id: str,
    principal: Principal = Depends(get_current_principal),
    repository: InMemoryItemRepository = Depends(get_item_repository),
) -> Response:
    deleted = await repository.delete_item(item_id=item_id, owner=principal.subject)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

