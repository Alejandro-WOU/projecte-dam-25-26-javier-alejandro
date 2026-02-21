package com.renaix.presentation.common.components

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Inbox
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.renaix.R
import com.renaix.ui.theme.Purple300

/**
 * Vista de estado vacío con logo decorativo de Renaix
 */
@Composable
fun EmptyStateView(
    title: String,
    message: String,
    modifier: Modifier = Modifier,
    icon: ImageVector = Icons.Filled.Inbox,
    actionText: String? = null,
    onAction: (() -> Unit)? = null,
    showLogo: Boolean = true
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        // Logo de Renaix como elemento decorativo
        if (showLogo) {
            Image(
                painter = painterResource(id = R.drawable.ic_renaix_logo),
                contentDescription = null,
                modifier = Modifier
                    .size(100.dp)
                    .alpha(0.15f),
                contentScale = ContentScale.Fit,
                colorFilter = ColorFilter.tint(Purple300)
            )

            Spacer(modifier = Modifier.height(16.dp))
        }

        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier.size(64.dp),
            tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f)
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = title,
            style = MaterialTheme.typography.titleLarge,
            color = MaterialTheme.colorScheme.onSurface,
            textAlign = TextAlign.Center
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = message,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center
        )

        if (actionText != null && onAction != null) {
            Spacer(modifier = Modifier.height(24.dp))

            Button(onClick = onAction) {
                Text(actionText)
            }
        }
    }
}
