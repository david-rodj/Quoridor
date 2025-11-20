from src.player.IPlayer import *
from src.action.IAction import *
from src.action.Quit    import *
import pygame



class Human(IPlayer):
    def play(self, board) -> IAction:
        if not INTERFACE:
            raise Exception("")
        showing_pawn = False
        showing_fence = False
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                if showing_pawn:
                    board.hideValidPawnMoves(self, board.storedValidPawnMoves[self.pawn.coord])
                if showing_fence:
                    board.hideValidFencePlacings(self, board.storedValidFencePlacings)
                return Quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # Hide fence if showing
                    if showing_fence:
                        board.hideValidFencePlacings(self, board.storedValidFencePlacings)
                        showing_fence = False
                    # Toggle pawn
                    if showing_pawn:
                        board.hideValidPawnMoves(self, board.storedValidPawnMoves[self.pawn.coord])
                        showing_pawn = False
                    else:
                        board.displayValidPawnMoves(self, board.storedValidPawnMoves[self.pawn.coord])
                        showing_pawn = True
                elif event.key == pygame.K_f and self.remainingFences() > 0:
                    # Hide pawn if showing
                    if showing_pawn:
                        board.hideValidPawnMoves(self, board.storedValidPawnMoves[self.pawn.coord])
                        showing_pawn = False
                    # Toggle fence
                    if showing_fence:
                        board.hideValidFencePlacings(self, board.storedValidFencePlacings)
                        showing_fence = False
                    else:
                        board.displayValidFencePlacings(self, board.storedValidFencePlacings)
                        showing_fence = True
                elif event.key == pygame.K_ESCAPE:
                    if showing_pawn:
                        board.hideValidPawnMoves(self, board.storedValidPawnMoves[self.pawn.coord])
                    if showing_fence:
                        board.hideValidFencePlacings(self, board.storedValidFencePlacings)
                    return Quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (showing_pawn or showing_fence):
                click_x, click_y = event.pos
                if showing_pawn:
                    pawnMove = board.getPawnMoveFromMousePosition(self.pawn, click_x, click_y)
                    if pawnMove is not None:
                        board.hideValidPawnMoves(self, board.storedValidPawnMoves[self.pawn.coord])
                        showing_pawn = False
                        return pawnMove
                elif showing_fence:
                    fencePlacing = board.getFencePlacingFromMousePosition(click_x, click_y)
                    if fencePlacing is not None:
                        board.hideValidFencePlacings(self, board.storedValidFencePlacings)
                        showing_fence = False
                        return fencePlacing

    def __str__(self):
        return "[HUMAN] %s (%s)" % (self.name, self.color.name)


