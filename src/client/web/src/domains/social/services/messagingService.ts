/**
 * Messaging Service
 * PRELIMINARY - To be updated when Social API is received
 */

import { socialApi } from '../api'
import type {
  Mailbox,
  MessageThread,
  Message,
} from '../models'

export class MessagingService {
  /**
   * Get complete mailbox (threads + messages)
   */
  async getMailbox(): Promise<Mailbox> {
    return socialApi.getMailbox()
  }
  
  /**
   * Get list of threads
   */
  async getThreads(): Promise<MessageThread[]> {
    return socialApi.getThreads()
  }
  
  /**
   * Get messages from a specific thread
   */
  async getThread(threadId: string): Promise<Message[]> {
    return socialApi.getThread(threadId)
  }
  
  /**
   * Create a new conversation
   */
  async createThread(title: string): Promise<MessageThread> {
    return socialApi.createThread({ title })
  }
  
  /**
   * Send a message in a thread
   */
  async sendMessage(threadId: string, content: string): Promise<Message> {
    return socialApi.sendMessage(threadId, { content })
  }
  
  /**
   * Get unread message count
   */
  async getUnreadCount(): Promise<number> {
    const threads = await this.getThreads()
    return threads.reduce((sum, thread) => sum + (thread.unreadCount || 0), 0)
  }
  
  /**
   * Check if there are unread messages
   */
  async hasUnreadMessages(): Promise<boolean> {
    const count = await this.getUnreadCount()
    return count > 0
  }
  
  /**
   * Mark thread as read
   * TODO: Implement when API is received
   */
  async markAsRead(threadId: string): Promise<void> {
    throw new Error('Not implemented yet')
  }
  
  /**
   * Delete a thread
   * TODO: Implement when API is received
   */
  async deleteThread(threadId: string): Promise<void> {
    throw new Error('Not implemented yet')
  }
}

// Singleton instance
export const messagingService = new MessagingService()
