package com.demperm.android

import org.junit.Test
import org.junit.Assert.*
import com.demperm.android.model.Proposal
import com.demperm.android.model.VoteType

/**
 * Example local unit test, which will execute on the development machine (host).
 *
 * See [testing documentation](http://d.android.com/tools/testing).
 */
class ExampleUnitTest {
    @Test
    fun addition_isCorrect() {
        assertEquals(4, 2 + 2)
    }
    
    @Test
    fun proposal_creation_isCorrect() {
        val proposal = Proposal(
            id = 1,
            title = "Test Proposal",
            description = "Test Description",
            votesYes = 10,
            votesNo = 5,
            votesAbstain = 2
        )
        
        assertEquals(1, proposal.id)
        assertEquals("Test Proposal", proposal.title)
        assertEquals("Test Description", proposal.description)
        assertEquals(10, proposal.votesYes)
        assertEquals(5, proposal.votesNo)
        assertEquals(2, proposal.votesAbstain)
        assertTrue(proposal.isActive)
    }
    
    @Test
    fun voteType_enum_isCorrect() {
        assertEquals(3, VoteType.values().size)
        assertEquals(VoteType.YES, VoteType.valueOf("YES"))
        assertEquals(VoteType.NO, VoteType.valueOf("NO"))
        assertEquals(VoteType.ABSTAIN, VoteType.valueOf("ABSTAIN"))
    }
}